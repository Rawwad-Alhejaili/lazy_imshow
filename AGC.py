#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Oct  4 21:11:08 2022

%GAIN: Gain a group of traces.
%
%  [dout] = gain(d,dt,option1,parameters,option2);
%
%  IN   d(nt,nx):   traces
%       dt:         sampling interval
%       parameters = [agc_gate], length of the agc gate in secs
%       option2 = 0  No normalization
%               = 1  Normalize each trace by amplitude
%               = 2  Normalize each trace by rms value
%
%  OUT  dout(nt,nx): traces after application of gain function
%
%
%  Example:
%
%    d = hyperbolic_events; dout = gain(d,0.004,'agc',0.05,1);
%    wigb([d,dout]);
%
%  Copyright (C) 2008, Signal Analysis and Imaging Group
%  For more information: http://www-geo.phys.ualberta.ca/saig/SeismicLab
%  Author: M.D.Sacchi
%
%  This program is free software: you can redistribute it and/or modify
%  it under the terms of the GNU General Public License as published
%  by the Free Software Foundation, either version 3 of the License, or
%  any later version.
%
%  This program is distributed in the hope that it will be useful,
%  but WITHOUT ANY WARRANTY; without even the implied warranty of
%  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
%  GNU General Public License for more details: http://www.gnu.org/licenses/
%
%     

@author: Rawwad Alhejaili (Python Code), M.D.Sacchi (Original MATLAB Code)
"""

import torch
# import torch.nn as nn
import torch.nn.functional as F

# class my_custom_func(torch.autograd.Function):
#     # Functions such as floor, ceil, and round have zero gradients everywhere
#     # which highly affects backward propagation. As such, this function was
#     # created to let the gradients simply pass through such functions.
#     # In other words, the gradients of said function will now be equal to one.
#     # Great explanation here: https://discuss.pytorch.org/t/torch-round-gradient/28628/4
    
#     # author: Zhonghzi_Yu (origianl author), Rawwad (slight modifications)
#     # link: https://discuss.pytorch.org/t/torch-round-gradient/28628/6
    
#     def __init__(self, func):
#         my_custom_func.func = func
    
#     @staticmethod
#     def forward(ctx, input):
#         ctx.input = input  #this does not seem to be necessary
#         return my_custom_func.func(input)
#         # return my_custom_func.func(input).long()  #gradients still do NOT propagate through variable of type long

#     @staticmethod
#     def backward(ctx, grad_output):
#         grad_input = grad_output.clone()
#         return grad_input

# class custom_floor(nn.Module):
#     def __init__(self):
#         super().__init__()
#         self.func = my_custom_func(torch.floor)
#     def forward(self, x):
#         return self.func.apply(x)

# class custom_ceil(nn.Module):
#     def __init__(self):
#         super().__init__()
#         self.func = my_custom_func(torch.ceil)
#     def forward(self, x):
#         return self.func.apply(x)

# class custom_round(nn.Module):
#     def __init__(self):
#         super().__init__()
#         self.func = my_custom_func(torch.round)
#     def forward(self, x):
#         return self.func.apply(x)

def AGC(d, dt, parameters, option2, return_gain_map=False):
    nt = d.shape[-2]
    device = d.device
    
    # L = parameters/dt+1
    # L = np.floor(L/2)
    # h = torch.tensor(triang(2*L+1).reshape(1,1,-1,1), dtype=d.dtype).to(device)
    
    L = torch.tensor(parameters/dt+1, dtype=d.dtype)
    L = torch.floor(L/2).long()
    h = (1-torch.linspace(-1, 1, 2*L+3).abs()[1:-1].reshape(1,1,-1,1)).type(d.dtype)
    
       
    # for k in range(nx):
    aux = d.clone()
    e = aux**2
    conv_e_h = F.conv2d(e, h.to(device), padding='same')
    rms = torch.sqrt(conv_e_h)
    epsi = 1e-10*rms.max()
    # a,b = rms, rms**2+epsi
    # non_zero_idx = b!=0
    
    # op = a.clone()
    # op = a / b
    # op[non_zero_idx] = a[non_zero_idx] / b[non_zero_idx]
    # op = np.divide(a, b, out=np.zeros_like(a), where=b!=0)
    gain_map = rms/(rms**2+epsi)
    dout = d * gain_map
    # print(dout.shape)
       
    if option2==1:                #% Normalize by amplitude 
        aux  = dout.clone().abs()
        amax = aux.max(dim=-2, keepdims=True)[0]
        zero_idx = amax==0
        amax[zero_idx] += 1 #Avoid zero division
        dout = dout / amax
        gain_map = gain_map / amax
       
       
    if option2==2:                # Normalize by rms 
        aux  = torch.pow(dout, 2)
        amax = aux.sum(dim=-2, keepdims=True)[0]
        amax = torch.sqrt(amax/nt)
        zero_idx = amax==0
        amax[zero_idx] += 1 #Avoid zero division
        # dout /= amax
        # gain_map /= amax
        dout = dout / amax
        gain_map = gain_map / amax
    
    if return_gain_map:
        return dout, gain_map
    else:
        return dout
