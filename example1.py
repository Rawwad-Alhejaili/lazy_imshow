#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Sep 28 17:31:32 2022

This is an example to demonstrate how the class lazy_imshow can be used.
For best results, try to run a single line at a time.

@author: Someone lazy :)
"""

from pathlib import Path #used to handle paths in a platform-agnostic way
from lazy_imshow import lazy_imshow
from patch import Patch  #used to patchify images
import numpy as np
import torch

# =============================================================================
# Initialization Example (All what you should need should be here)
# =============================================================================
# To show shot gathers, the aspect ratio must be modified (otherwise, it will 
# be too thin). Also, we will clip the minimum and maximum 1% of its histogram
# to improve the visibility of the image.
lazy_shot = lazy_imshow(cmap   = 'seismic_r', 
                        aspect = 1/3,
                        clip   = 1)

# For showing patches however, we do not need to modify the aspect ratio, so we
# can save ourselves the trouble of writing that over and over again by 
# initializing another lazy_imshow instance (you could see why its "lazy":)
lazy_patch = lazy_imshow(cmap = 'seismic_r', 
                         clip = 1)

imshow_shot = lazy_shot.imshow
imshow_patch = lazy_patch.imshow

#%%
# =============================================================================
# Load some images
# =============================================================================
cwd = Path.cwd()  #current working directory path
Im_path = cwd / 'Images' / 'Mobil_AVO_Viking_Graben_Line_12.npy'  #path to the data
Im = np.load(Im_path)  # (5,1,1500,120)

# Below, we will convert the image to a tensor and move it to the GPU just to
# demonstrate that the imshow function will still work regardless of the input
# type or whether it is on the GPU or CPU (or whether it has gradients or not)
device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
Im = torch.tensor(Im).to(device)  #convert it to a tensor 

shots = [Im[i] for i in range(4)]  #store only the first 4 shot gathers
shots_titles = [f'Shot {i}' for i in range(4)]
P = Patch(extraDim=1)
Im_patch = P.patchify(Im, patch_size=(120,120), stride=300) #(N,N_patch,C,H,W)
patches = [Im_patch[:1,i] for i in range(1,5)]  #only store 4 patches from
                                                #the first shot
patches_titles = [f'Patch {i}' for i in range(4)]

#%%
# =============================================================================
# Show the images
# =============================================================================
# First, let's show a single shot
imshow_shot(shots[0], title=shots_titles[0])
# Note: you can decrease the padding between the colorbar and the image

# Show a single shot, but without clip
imshow_shot(shots[0], title='No clip', clip=0)

# Show a single patch
imshow_patch(patches[0], title=patches_titles[0])

# Show mulitple shots in different grids
imshow_shot(shots, title=shots_titles, grid=(1,4))
imshow_shot(shots, title=shots_titles, grid=(2,2))

# Show mulitple patches
imshow_patch(patches, title=patches_titles, grid=(2,2))

# See how the clarity is messed up? This is the results of the seismic image
# having a very wide range, so let's try to fix it

# There are multiple ways to edit the range shown in the grid:
# - Use the range of an existing image
#   - If you wish to use the range of the Nth image, then set rang=N-1
imshow_patch(patches, title=patches_titles, grid=(2,2), rang=-1)#use last image
# - Using a fixed range
#   - To use a range of a to b, then set rang = (a,b)
imshow_patch(patches, title=patches_titles, grid=(2,2), rang=(-80,80))
# - Using the global range (global minimum and maximum)
#   - To use the global range of all images, then rang='global'
imshow_patch(patches, title=patches_titles, grid=(2,2), rang='global')
# - Normalizing each image
#   - Set rang = 'norm'
imshow_patch(patches, title=patches_titles, grid=(2,2), rang='norm')

# Now, what would occur if we did not specify a grid (nor a title)?
imshow_patch(patches) #all image will be show in a single row with no titles
                      #in other words, the function will not freak out

# How can we remove an image from the grid?
# For example, if we we have a grid=(3,3), and we want to remove the image at
# subplot(3,3,5), how would we achieve this?
# First generate enough patches
patch_9 = P.patchify(Im, patch_size=(120,120), stride=120) #(N,N_patch,C,H,W)
patch_9 = [patch_9[:1,i] for i in range(9)]
# To remove the image at index = 4, then simply set that image to zero and set
# ignoreZeroStd = True
patch_9[4] = 0*patch_9[4]
imshow_patch(patch_9, grid=(3,3), rang='global', ignoreZeroStd=True)

# Can we "temporarily" change an argurment saved during the initialization?
# To investigate this, we will use imshow_shot to display patches.
# Then, we will show it as is, but change the aspect argument set to 1
imshow_shot(patches, title=patches_titles, grid=(2,2), rang='norm')
imshow_shot(patches, title=patches_titles, grid=(2,2), rang='norm', aspect=1)

# =============================================================================
# Playgorund
# =============================================================================
'''
Now, you have seen the essentials of this function. As such, I will list all 
the arguments that can be used below. You can play with the different 
arguments here if you find any of them to be interesting. Though, keep the 
following bugs in mind:
Known Bugs:
- `plotsize` argument might be inconsistent depending on the aspect ratio of the images.
- `cbar_ticks` sometimes does not _obey_ orders and decides to use its own number of ticks.
- `alphabet` only works when the images are shown in a single row.
- The colorbar uses the range and colormap of the last plot.
'''

lazy_play = lazy_imshow(I              = None, 
                        title          = '', 
                        grid           = (1,1), 
                        colorbar       = True, 
                        cbar_ticks     = 11,
                        aspect         = 1/3,
                        cmap           = 'seismic_r', 
                        pad            = 0.7, 
                        plotsize       = (10,10), 
                        rang           = -1, 
                        dpi            = 300, 
                        figTransparent = False, 
                        fontsize       = 14, 
                        alphabet       = False,
                        ignoreZeroStd  = True, 
                        clip           = 0)

imshow_play = lazy_play.imshow

