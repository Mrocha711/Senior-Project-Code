#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Oct 11 17:22:01 2025

@author: 
"""


# imports
import numpy as np
import pandas as pd

# Global Intializations 
mortar_joint_size = 0.375
types = np.array(["M","S","N"])

rebar_dataframe = pd.read_excel("Masonry_Tables.xlsx", sheet_name="Rebar_Size")
fr_beam_dataframe = pd.read_excel("Masonry_Tables.xlsx", sheet_name="fr_beam", index_col=0)
net_area_comp_strength_clay_dataframe = pd.read_excel("Masonry_Tables.xlsx", sheet_name="net_area_comp_strength_clay")
net_area_comp_strength_concrete_dataframe = pd.read_excel("Masonry_Tables.xlsx", sheet_name="net_area_comp_strength_concrete")

# Classes
class Block:
    def __init__(self, thickness , CMU_size , mortar_type):
        
        self.thickness = thickness
        self.block_height, self.block_width, self.block_length = [int(x)-mortar_joint_size for x in CMU_size.split("x")]  

        #if unit is less than 4 in use  85% of value listed
        size_factor = 1
        if self.block_height or self.block_width or self.block_length < 4:
            size_factor = 0.85
            
        # Table gives relationship between net compressive strength of masonry and mortar strength
        self.mortar_type = mortar_type
        
        
# Testing code DELETE LATER
b1 = Block(8, "8x8x16","N")
print(b1.block_height)

class Column: #element_dataframe
    def __init__(self, user_input_block , user_input_height , user_input_grouting , f_m_overwrite ):
        #height
        self.height = user_input_block.block_height
        #thickness 
        self.thickness = user_input_block.thickness
        
        # grouting
        # fr_beam_dataframe.user_input_block.mortar_type (amount like partially grouted, type like mortar type)
        self.grouting = fr_beam_dataframe.loc[str(user_input_grouting)].user_input_block.mortar_type
        
        self.courses = 2 #read user input of amount of masonry courses used
        self.f_m = 2 #ksi ?
        
        # Reinforcement properties
        # TODO how do get visual input from user ie block dwg
        self.f_y = 60 #ksi should apply user input for rebar ?
        self.A_st = 10 # user_reinf_input_num_bars * total_bar_area based on rebar_dataframe
        
        


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
# thickness >= 8"
# h/r < 99
# course Length < 6t

# 6" spacing limit between unsupported  bars TMS 5.4.1.4


#  P-M interaction code (import from seperate file)

# compare P-M interaction to actual 

# make a user_input_block code snippet

# user_input_block = Block(a , b ,c )
# user_input_grouting -> dropdown menu to choose grouting options out of the possible four


# Resources
# https://pandas.pydata.org/pandas-docs/stable/user_guide/indexing.html
# chrome-extension://efaidnbmnnnibpcajpcglclefindmkaj/https://structurepoint.org/pdfs/manuals/spcolumn-manual.pdf
# https://www.calctree.com/resources/interaction-diagram
# https://docs.masonryanalysisstructuralsystems.com/walls/a-complete-wall-design/
# https://docs.masonryanalysisstructuralsystems.com/walls/p-m-interaction-diagram/#P-M_Interaction_Diagram_Reinforced_Masonry

