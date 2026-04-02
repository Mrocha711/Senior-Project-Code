#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Mar 31 14:51:50 2026

@author: alisaleh
"""

# HOW TO MAKE P-M interaction Diagram

# imports
import numpy as np
import sympy as sy

#ignore unreinforced axial tension effecs based on TMS code provisions

e_m = 0.0025
phi_axial = 0.65
phi_mmn = 0.65 #minimum 
E = 29000 #ksi

    
def createPM_masonry(masonry_block, reinf_boolean, element_dataframe):
    
    #variable import dump
    h = element_dataframe.height
    A_n = masonry_block.thickness * element_dataframe.courses * masonry_block.block_width
    r = masonry_block.block_length / (np.sqrt(12))
    f_m = element_dataframe.f_m
    A_st = element_dataframe.A_st
    f_y = element_dataframe.f_y
    e_ty = element_dataframe.f_y/E
    
    # Variables for each case:
    P_n = 0 #pure axial
    M_n = 0 #pure moment
    P_nu, M_nu = 0 #balance point
    
    # PURE AXIAL CASE [0, Pn]
    if(h/r <= 99):
        # TMS 402 9.3.3.1 a
        P_n = 0.8(0.8 * (A_n - A_st) * (f_m) + (A_st * f_y) )*( 1 - (h/(140*r))**2 )
    if(h/r > 99):
        # TMS 402 9.3.3.1 b
        P_n = 0.8*(0.8 * (A_n - A_st) * (f_m) + (A_st * f_y) ) * ((70*r)/h)**2 
    
    if (reinf_boolean == False):  
    # unreinforced axial  
        if(h/r <= 99):
            # TMS 402 9.2.4.1 a
            P_n = 0.8(0.8 * (A_n) * (f_m) * ( 1 - (h/(140*r))**2 ))
        if(h/r > 99):
            # TMS 402 9.2.4.1 b
            P_n = 0.8*(0.8 * (A_n) * (f_m) * ((70*r)/h)**2 )

    # PURE MOMENT CASE [Mn, 0]
    #c = sy.symbols('c') // approximate c
    #c = (A_st * f_y)/(0.64 * element_dataframe.thickness * f_m)
    c = 0.01
    T = 0
    # C_m = 0.64 * f_m * c * masonry_block.thickness
    C_m = 0.64 * f_m * c * masonry_block.thickness
    
    while ( round(T - C_m,3) != 0):
        
        c = c + 0.001
        # for each reinforcement depth
        for layer_depth in element_dataframe.reinf_depth:
            # compute: e_layer[i] = e_m * (layer_depth[i] - c)/c
            e_layer = e_m * (layer_depth - c)/c
            # compute: F_s[i] = e_m[i] * A_s * f_y
            f_s_layer = e_layer * A_st * f_y
            #if greater than A_s*f_y , set equal to A_s*f_Y
            if (f_s_layer > A_st*f_y):
                f_s_layer = A_st*f_y
                
            T = T + f_s_layer
            
            #compute phi factor for moments: TMS 402, Table 9.1.4
            if (e_layer > e_ty + 0.003):
                phi_m = 0.9
            elif (e_ty < e_layer < e_ty+0.003 ):
                phi_m = 0.65 + (e_layer-e_ty)*0.25/(0.003)

        # if (reinf_boolean == False): T = 0
        if (reinf_boolean == False):
            T = 0
            return('Masonry Reinforcement Required')
            break
    
    # Compute M_n
    M_t_tot = 0
    for layer_depth in element_dataframe.reinf_depth:
        # compute: e_layer[i] = e_m * (layer_depth[i] - c)/c
        e_layer = e_m * (layer_depth - c)/c
        # compute: F_s[i] = e_m[i] * A_s * f_y
        f_s_layer = e_layer * A_st * f_y
        #if greater than A_s*f_y , set equal to A_s*f_Y
        if (f_s_layer > A_st*f_y):
            f_s_layer = A_st*f_y
        
        M_ts = f_s_layer * (layer_depth - (0.5*element_dataframe.block_width*element_dataframe.courses))  
        M_t_tot = M_t_tot + M_ts
    
    M_n = C_m * ((0.5*element_dataframe.block_width*element_dataframe.courses)-(0.4*c)) + M_t_tot

    
    # compute the balance point
    
    # interpolate between the balance point and the M_n point and P_n point based on strain

    
    #return P_m diagram data

    