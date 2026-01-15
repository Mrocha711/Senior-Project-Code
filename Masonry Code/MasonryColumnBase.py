#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Oct 11 17:22:01 2025

@author: 
"""


# imports
import numpy as np



# Global Variables
mortar_joint_size = 0.375
types = np.array(["M","S","N"])


# Classes
class block:
    def __init__(self, thickness , CMU_size , mortar_type):
        
        self.thickness = thickness
        self.block_height, self.block_width, self.block_length = [int(x)-mortar_joint_size for x in CMU_size.split("x")]  

        #if unit is less than 4 in use  85% of value listed
        size_factor = 1
        if self.block_height or self.block_width or self.block_length < 4:
            size_factor = 0.85
            
        
        # import masonry table
        # Table gives relationship between net compressive strength of masonry and mortar strength


# Testing code
b1 = block(8, "8x8x16","N")
print(b1.block_height)

#class column: 
#    def __init__(self, block , height , grouting  ):
        

# height
# thickness
# grouting
# 

# Masonry Block
# f'm

# reinforcement
# Fy steel 

# loading properties
# Pu
# Mu
# add self weight

# load combos
#


# COLUMN ANALYSIS

# Dimension limits
