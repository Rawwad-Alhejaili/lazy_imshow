#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Mar 19 17:30:03 2022

This class patchifies the tensor into different patches, and provides an
unpatchificiation function that is simple and quick to use.

Notes:
    - The function is not perfect yet. Errors could rise if the image is not
      neatly divided into patches.
    - Not sure if I have tested the use of non-square patches.
    - The class loads the tensor to the CPU to avoid using the VRAM.
    - It works on 4D tensors

@author: ruwwad
"""

import numpy as np
import torch
from tqdm import tqdm

from gaussian2d import gaussian2d
from pyramid2d import pyramid2d

pr = lambda a,b: print('{}.shape = {}'.format(a, b.shape))
class Patch():
    def __init__(self, extraDim=0):
        self.Dim = extraDim  #Added dimensions
    def patchify(self, I, patch_size, stride):
        self.org_shape = I.shape
        device = I.device
        I = I.to('cpu')  #Could possibly save a little bit of VRAM this way
        xMax, yMax = patch_size
        N = I.shape[0]
        patchX = int(np.ceil((I.shape[-2] - xMax + 1) / stride))
        patchY = int(np.ceil((I.shape[-1] - yMax + 1) / stride))
        # patchZ = int(np.ceil(I.shape[1] / strideChn))  #I am not sure about this
        n_patches = patchX*patchY
        patches = torch.zeros((N, n_patches,I.shape[1],xMax,yMax))
        self.patchX = patchX
        self.patchY = patchY
        # self.patchZ = patchZ
        self.xMax = xMax
        self.yMax = yMax
        self.stride = stride
        # print('patchX =', patchX)
        # print('patchY =', patchY)
        # print('patchZ =', patchZ)
        # print('patch.shape =', patches.shape)
        counter = 0
        for n in range(N):
            for i in range(patchX):
                for j in range(patchY):
                    # try:
                        # print('n =', n)
                        # print('k =', k)
                        # print('Counter =',counter)
                        # print('i =',i)
                        # print('j =',j)
                        # print('k =',k)
                        # print('k*(patchX*patchY)+patchY*i+j=', k*(patchX*patchY)+patchY*i+j)
                        # print('stride*i:stride*i+xMax =', np.arange(stride*i, stride*i+xMax+1))
                        
                        # print('I = \n{}'.format(I[k, 0, stride*i:stride*i+xMax
                        #                             ,stride*j:stride*j+yMax]))
                        # I[n,  0,  stride*i:stride*i+xMax  ,stride*j:stride*j+yMax]
                        patches[n, patchY*i+j, :] \
                            = I[n, :, stride*i:stride*i+xMax, stride*j:stride*j+yMax]
                        counter += 1
            # print(counter)
        self.patches_shape = patches.shape  #Used to reshape 4D patches back to 5D
        self.n_patches = patches.shape[1]
        if self.Dim == 0: #Then merge the number of samples and patches
            shap = [int(patches.shape[0] * patches.shape[1])]
            for i in patches.shape[2:]:
                shap.append(i)
            # pr('patches', patches)
            # print('mergedShape =', shap)
            patches = patches.reshape(shap)
        return patches.to(device)
    def unpatchify(self, I, weight='pyramid', std=22):
        device = I.device
        I = I.to('cpu')
        I = I.reshape(self.patches_shape)
        N      = I.shape[0]
        patchX = self.patchX
        patchY = self.patchY
        # patchZ = self.patchZ
        xMax   = self.xMax
        yMax   = self.yMax
        stride = self.stride
        out_shape = self.org_shape
        # print('org.shape =', out_shape)
        # n_patches = patchX*patchY
        # pr('  I', I)
        out  = torch.zeros((N, I.shape[2], out_shape[-2], out_shape[-1]))
        self.norm = torch.clone(out)
        if weight == 'gaussian':
            weight = gaussian2d(I.shape, std)
            weight = weight[:,0]+1
        elif weight == 'pyramid':
            weight = pyramid2d(I.shape)
            weight = weight[:,0]+1
        else:
            weight = 0*torch.clone(I)
            weight = weight[:,0]+1
        # pr('out', out)
        # print('patchX =', patchX)
        # print('patchY =', patchY)
        # print('patchZ =', patchZ)
        # print('patch.shape =', patches.shape)
        counter = 0
        # print('patchX =', patchX)
        # print('patchY =', patchY)
        # for k in range(I.shape[1]):
        for i in tqdm(range(patchX), desc='Unpatchifying'):
            for j in range(patchY):
                # print('I[:, counter] =', I[:, counter].shape)
                # pr(' weight', weight)
                out[:,:,stride*i:stride*i+xMax, stride*j:stride*j+yMax] \
                    += I[:, counter] * weight
                self.norm[:,:,stride*i:stride*i+xMax, stride*j:stride*j+yMax] \
                    += weight
                # print(f'out = \n{out}')
                # print(f'self.norm = \n{self.norm}')
                counter += 1
        # print(f'self.norm = \n{self.norm}')
        # pr('self.norm', self.norm)
        # pr('weight', weight)
        # self.norm = self.norm.sum(dim=1); print(f'self.norm = \n{self.norm}')
        # return (out.sum(dim=1) / self.norm.sum(dim=1)).to(device)
        out = out / self.norm  #This could perform 0/0, which will yield NaN
        
        if torch.isnan(out).any():
            print('''WARNING: The alogrithm produced NaN!
                  
This happened because the image does not neatly fit into patches.
To fix this, change either the dimensions of the original image
(by cropping or reshaping), or by choosing another patch dimensions
that fit the image perfectly.

For now though, we will set the NaN to zero to avoid further complications.

This problem "might" be addressed in a future update.''')
        
        # The algorithm could produce NaN due to division by zero (I guess).
        # To circumvent this, each NaN will be set to zero.
        # We use the property [NaN != NaN] to find the NaNs and set them to 0.
        out[out != out] = torch.zeros(out[out != out].shape)
        self.norm = self.norm[0,0] #To decrease the memory usage
        return out.to(device)


# =============================================================================
# Example
# =============================================================================
# P = Patch()
# t = torch.arange(2*5*3*2).reshape([2,2,5,3]).cuda()
# # t = torch.arange(1*1*4*3).reshape([1,1,4,3]).cuda()
# I, xMax, yMax, stride = [t, 2, 2, 1]

# bat = P.patchify(t, (3,3), stride)
# org = P.unpatchify(bat, 'gaussian')
# # org = P.unpatchify(bat, 'avg')

# print('t.shape =', t.shape)
# print('Im2patch.shape =', bat.shape)
# print('patch2Im.shape =', org.shape)

# # Below we will run two assertions to make sure that the function is working as 
# # intended. Interestingly, for gaussian unpatchification, it cannot pass the
# # second assertion despite passing the first assertion. This is the case 
# # because even though the loss is very minimal, it is not an exact zero and as 
# # such, it cannot pass the the second assertion

# assert ((t/org)[t/org == t/org]).mean().item() == 1
# assert ((org-t)**2).sum().item() == 0

# Numpy implementation (check dimensions if you wish to implement it)
# =============================================================================
# def batches(I, xMax, yMax, stride, strideChn=1):
#     patchX = int(np.ceil((I.shape[1] - xMax + 1) / stride))
#     patchY = int(np.ceil((I.shape[2] - yMax + 1) / stride))
#     patchZ = int(np.ceil(I.shape[0] / strideChn))
#     patches = np.zeros((patchX*patchY*patchZ,xMax,yMax))
#     print('patchX =', patchX)
#     print('patchY =', patchY)
#     print('patchZ =', patchZ)
#     counter = -1
#     for k in range(patchZ):
#         for i in range(patchX):
#             for j in range(patchY):
#                 try:
#                     patches[k*(patchX*patchY)+patchY*i+j,:,:] = I[k, stride*i:stride*i+xMax
#                                                ,stride*j:stride*j+yMax]
#                     counter += 1
#                     # print('Counter =',counter)
#                     # print('i =',i)
#                     # print('j =',j)
#                     # print('k =',k)
#                     # print('k*(patchX*patchY)+patchY*i+j=', k*(patchX*patchY)+patchY*i+j)
#                 except:
#                     # print('Counter =',counter)
#                     # print('i =',i)
#                     # print('j =',j)
#                     # print('k =',k)
#                     # print('k*(patchX*patchY)+patchY*i+j=', k*(patchX*patchY)+patchY*i+j)
#                     # print(patches)
#                     break;break;break
#     print(counter)
#     return patches
# =============================================================================

# Example:
# =============================================================================
# m,n = 8,8
# I = np.arange(m*n).reshape(m,n)
# print(I)
# print()
# xMax, yMax = 4, 4
# stride = 2
# patchX = int(np.ceil((I.shape[0] - xMax + 1) / stride))
# patchY = int(np.ceil((I.shape[1] - yMax + 1) / stride))
# 
# Im = np.zeros((patchX*patchY,xMax,yMax))  #Fix this
# 
# for i in range(patchX):
#     for j in range(patchY):
#         Im[patchX*i+j,:,:] = I[stride*i:stride*i+xMax
#                               ,stride*j:stride*j+yMax]
# print(Im)
# =============================================================================
