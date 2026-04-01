#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Mar 31 14:51:50 2026

@author: alisaleh
"""

# HOW TO MAKE P-M interaction Diagram

# imports
import numpy as np


#ignore unreinforced axial tension effecs

#ecu = 0.003
#phi axial = 0.65

#Step 1: develop pure axial point
    
def createPM_masonry(masonry_block, reinf_boolean, element_dataframe):
    
    #variable import dump
    h = element_dataframe.height
    A_n = masonry_block.thickness * element_dataframe.courses * masonry_block.block_width
    r = masonry_block.block_length / (np.sqrt(12))
    f_m = element_dataframe.f_m
    
    #pure axial equation add for reinforced masonry
    P_n = 0
    
    if (reinf_boolean == False):  
    # unreinforced axial + flexural 
        if(h/r <= 99):
            P_n = 0.8(0.8 * (A_n) * (f_m) * ( 1 - (h/(140*r))**2 ))
        if(h/r > 99):
            P_n = 0.8*(0.8 * (A_n) * (f_m) * ((70*r)/h)**2 )

    #return P_m diagram data