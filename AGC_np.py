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

@author: Ruwwad Alhejaili (Python), M.D.Sacchi (MATLAB Code)
"""

import numpy as np
from scipy.signal import triang
from scipy.signal import convolve2d as conv2

def AGC_np(d, dt, parameters, option2, return_gain_map=False):
    nt,nx= d.shape[-2], d.shape[-1]
   
    dout = np.zeros(d.shape, dtype= d.dtype)
    gain_map = np.zeros(d.shape, dtype= d.dtype)
    L = parameters/dt+1
    L = np.floor(L/2)
    h = triang(2*L+1).reshape(-1,1)
       
    for k in range(nx):
        aux =  d[:,k:k+1]
        e = aux**2
        rms = np.sqrt(conv2(e,h,'same'))  #why use 2D conv to a 1D signal?
        epsi = 1e-10*rms.max()
        a,b = rms, rms**2+epsi
        op = np.divide(a, b, out=np.zeros_like(a), where=b!=0)
        # op = rms/(rms**2+epsi)
        dout[:,k:k+1] = d[:,k:k+1]*op
        gain_map[:,k:k+1] = op
    # print(dout.shape)
       
    if option2==1:                #% Normalize by amplitude 
        for k in range(nx):
            aux  = dout[:,k:k+1]
            amax = np.max(np.abs(aux))
            amax = amax or 1  #Avoid zero division
            dout[:,k] = dout[:,k]/amax
            gain_map[:,k] = gain_map[:,k]/amax
       
       
    if option2==2:                # Normalize by rms 
        for k in range(nx):
            aux  = dout[:,k]
            amax = np.sqrt(np.sum(aux**2)/nt)
            amax = amax or 1  #Avoid zero division
            dout[:,k] = dout[:,k]/amax
            gain_map[:,k] = gain_map[:,k]/amax
        
    if return_gain_map:
        return dout, gain_map
    else:
        return dout
