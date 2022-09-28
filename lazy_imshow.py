#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Sep 10 21:45:47 2022

This is simply a wrapper for imshow.py. The goal behind it is to store
your defaults only once. For example, I need to constantly show a grid of 2x2
with no color bar, and also have to show a grid of 1x4 that DO include a color
bar. Instead of having to change the arguements for each case, I can now define 
2 imshow instances with different defaults so I don't have to constantly change 
the arguements back and forth (which can still be temporarily overwritten even 
after setting the new defaults).

@author: Someone lazy :)
"""

from copy import deepcopy  #to copy the image regardless of whether its numpy or tensor
from imshow import imshow

class lazy_imshow():
    def __init__(self, 
                 I              = None, 
                 title          = None, 
                 grid           = (1,1), 
                 colorbar       = True, 
                 cbar_ticks     = 11, 
                 aspect         = 1,
                 cmap           = 'seismic_r', 
                 pad            = 0.7, 
                 plotsize       = (7,7), 
                 rang           = 'global', 
                 rangZeroCenter = False, 
                 dpi            = 300, 
                 figTransparent = False, 
                 fontsize       = 14, 
                 alphabet       = False,
                 ignoreZeroStd  = False,  
                 clip           = 0,
                 **kwargs):
        #Store the defaults in self
        self.I              = I
        self.title          = title
        self.grid           = grid
        self.colorbar       = colorbar
        self.cbar_ticks     = cbar_ticks
        self.aspect         = aspect
        self.cmap           = cmap
        self.pad            = pad
        self.plotsize       = plotsize
        self.rang           = rang
        self.rangZeroCenter = rangZeroCenter
        self.dpi            = dpi
        self.figTransparent = figTransparent
        self.fontsize       = fontsize
        self.alphabet       = alphabet
        self.ignoreZeroStd  = ignoreZeroStd
        self.clip           = clip
        
    def imshow(self, 
             I              = None,
             title          = None, 
             grid           = None, 
             colorbar       = None, 
             cbar_ticks     = None, 
             aspect         = None,
             cmap           = None, 
             pad            = None, 
             plotsize       = None, 
             rang           = None, 
             rangZeroCenter = None, 
             dpi            = None, 
             figTransparent = None, 
             fontsize       = None, 
             alphabet       = None, 
             ignoreZeroStd  = None, 
             clip           = None,
             **kwargs):
        
        # If the arguements are not changed, use the defaults from __init__
        if I is None:
            I     = deepcopy(self.I)
        if title          == None:
            title = deepcopy(self.title)
        if grid           == None:
            grid           = self.grid
        if colorbar       == None:
            colorbar       = self.colorbar
        if cbar_ticks     == None:
            cbar_ticks     = self.cbar_ticks
        if aspect         == None:
            aspect         = self.aspect
        if cmap           == None:
            cmap           = self.cmap
        if pad            == None:
            pad            = self.pad
        if plotsize       == None:
            plotsize       = self.plotsize
        if rang           == None:
            rang           = self.rang
        if rangZeroCenter == None:
            rangZeroCenter = self.rangZeroCenter
        if dpi            == None:
            dpi            = self.dpi
        if figTransparent == None:
            figTransparent = self.figTransparent
        if fontsize       == None:
            fontsize       = self.fontsize
        if alphabet       == None:
            alphabet       = self.alphabet
        if ignoreZeroStd  == None:
            ignoreZeroStd  = self.ignoreZeroStd
        if clip           == None:
            clip           = self.clip
        
        # Show the image
        imshow(I,
             title,
             grid,
             colorbar,
             cbar_ticks,
             aspect,
             cmap,
             pad,
             plotsize,
             rang,
             rangZeroCenter,
             dpi,
             figTransparent,
             fontsize,
             alphabet,
             ignoreZeroStd,
             clip,
             **kwargs)
        # Note:
        # When calling imshowSeismic2, I could have used "named" arguements to
        # to avoid errors in the future (if I update the locations of 
        # imshowSeismic2's arguements, then errors will be raised). However, I
        # have intentionally did it this way to catch errors early on.

# # =============================================================================
# # Initialization Example
# # =============================================================================
# lazy = lazy_imshow(I              = None, 
#                    title          = '', 
#                    grid           = (1,1), 
#                    colorbar       = True, 
#                    cbar_ticks     = 11,
#                    aspect         = 1,
#                    cmap           = 'seismic_r', 
#                    pad            = 0.7, 
#                    plotsize       = (10,10), 
#                    rang           = -1, 
#                    rangZeroCenter = False, 
#                    dpi            = 300, 
#                    figTransparent = False, 
#                    fontsize       = 14, 
#                    alphabet       = False,
#                    ignoreZeroStd  = True, 
#                    clip           = 0)

# imshow = lazy.imshow
# # Now call imshow(yourImages) to display the images with your default
# # parameters. Note that you can temporarily override the default parameters.
# # For example, assume we have a grid of (1,4), and we would like to change it
# # to (2,2), then call:
    
# # imshow(yourImage, grid=(2,2))

# # Now the image will be displayed your chosen grid. 
# # If you wish to permenantly change the default parameters, then you will have 
# # to call lazyImshow again.