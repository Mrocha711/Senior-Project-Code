#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Mar 31 14:51:50 2026

@author: alisaleh
"""

# HOW TO MAKE P-M interaction Diagram

# imports
import numpy as np
import matplotlib.pyplot as plt

def createPM_masonry(masonry_block, reinf_data, element_dataframe ):
    
    e_m = 0.0025
    phi_min = 0.65
    phi_max = 0.9 
    E = 29000 #ksi

    #variable import dump
    h = element_dataframe.height
    A_n = masonry_block.thickness * element_dataframe.courses * masonry_block.block_width
    r = masonry_block.block_length / (np.sqrt(12))
    f_m = element_dataframe.f_m
    A_st = element_dataframe.A_st
    f_y = element_dataframe.f_y
    e_ty = f_y/E
    #ratio_e = (e_m)/(e_m + e_ty)
    
    # Variables for each case:
    P_n, Pn, Mn, phi_Pn, phi_Mn, e_s = 0, [], [], [], [], [] #pure axial , pure moment , balance point

    # PURE AXIAL CASE [0, Pn]
    reinf_bool = reinf_data.boolean
    if (reinf_bool == True):
        if(h/r <= 99):
            # TMS 402 9.3.3.1 a
            P_n = 0.8*(0.8 * (A_n - A_st) * (f_m) + (A_st * f_y) )*( 1 - (h/(140*r))**2 )
        elif(h/r > 99):
            # TMS 402 9.3.3.1 b
            P_n = 0.8*(0.8 * (A_n - A_st) * (f_m) + (A_st * f_y) ) * ((70*r)/h)**2 
    elif (reinf_bool == False):  
    # unreinforced axial  
        if(h/r <= 99):
            # TMS 402 9.2.4.1 a
            P_n = 0.8*(0.8 * (A_n) * (f_m) * ( 1 - (h/(140*r))**2 ))
        elif(h/r > 99):
            # TMS 402 9.2.4.1 b
            P_n = 0.8*(0.8 * (A_n) * (f_m) * ((70*r)/h)**2 )
    
    #--------------------------------------------------------------------------
    # Creating P-M diagram (step by step)
    section_length = masonry_block.block_length * element_dataframe.courses
    #Step 1: Estiamte c - neutral axis depth (cannot be less than 0 or greater than the depth)
    num_of_iterations = 3000
    # steps: (section_length - 0) / num of steps 
    c_step = section_length/num_of_iterations
    
    for i in range (num_of_iterations):
        M_t = 0
        T_s = 0
        
        if i == 0:
            c = c_step
        else:
            c = c + c_step
 
        #Step 2: Compute C_m = 0.64 * f_m * c * masonry_block.thickness
        C_m = 0.64 * f_m * c * masonry_block.block_width

        e_steel = 0
        #Step 3: Compute x ie depth of reinfrocement 
        for lay_id, layer_depth in enumerate(reinf_data.reinf):
            # compute: e_layer[i] = e_m * (layer_depth[i] - c)/c
            e_layer = e_m * (layer_depth[1]-c)/c

            #Step 4: Compute the total force applied by the each steel bar 
            A_bar = layer_depth[0]
            
            #compute: F_s[i] = e_m[i] * A_s * E
            #f_s_layer = e_layer * A_bar * E
            # np.sign(es)*min(abs(es)*Es, fy)
            #if greater than A_s*f_y , set equal to A_s*f_Y
            #if (f_s_layer > A_bar*f_y):
            #    f_s_layer = A_bar*f_y
            #elif f_s_layer < -(A_bar*f_y):
            #    f_s_layer = -(A_bar*f_y) 
            f_s_layer = np.sign(e_layer)*min(abs(e_layer)*E,f_y)*A_bar
            #print(f_s_layer)
            #Step 5: Compute T, the total tension force 
            T_s += f_s_layer
            #Step 7.1 Compute moment contribution due to tension
            # if layer depth > c, layerdepth - section_length/2
            M_t += f_s_layer * (layer_depth[1] - section_length/2)
            e_steel = e_layer
            
        # if (reinf_boolean == False): T = 0
        if (reinf_bool == False):
            return('Masonry Reinforcement Required')
            T_s = 0
        #Step 6: Calculate Axial force through equilibruim
        P_nu = C_m - T_s
        #Step 7/8: Calculate Moment: (M_tension + M_compression)
        M_nu = M_t + (C_m * ( (section_length/2)-(0.8*c/2) )) 
 

        #Step 9: Compute Phi and ensure it does not exceed limits
        #print(e_steel)
        if (e_steel<= e_ty): # e_m = 0.0025
            phi = phi_min
        elif(e_steel >= e_ty+0.003): # e_ty = 0.00206 + 0.003 = 0.005
            phi = phi_max
        else:
            #TMS 402, Table 9.1.4
            phi = 0.65 + 0.25*(e_steel - e_ty)/(0.003)     
            #print(phi)
            
        #Step 10: Compute Phi * moment and Phi * axial 
        phi_Mn.append(phi * M_nu) #k-in
        Mn.append(M_nu) #k-in
        phi_Pn.append(phi * P_nu)
        Pn.append(P_nu)
        e_s.append(e_steel)

    #--------------------------------------------------------------------------
    #Step 11: plot data to form a curve 
 
    return phi_min*P_n, P_n, Pn, phi_Pn, Mn, phi_Mn, e_s
        
#------------------------------------------------------------------------------------        
# Test classes

class testReinf:
    def __init__(self, num , boolean ):
        self.boolean = boolean #true/false
        self.reinf = [
            [0.79*2, 3.5], #bar area (in^2), bar depth in.
            [0.79*2, 11.708],
            [0.79*2, 19.916],
            [0.79*2, 28.125],
            ]
        
class testBlock:
    def __init__(self, num  ):
        self.thickness = 8-0.375 #in
        self.block_length = 16-0.375 #in
        self.block_width = 16-0.375 #in
        
        
class testElement:
    def __init__(self, num ):
        self.courses = 2
        self.height = 30 #ft
        self.A_st = 0.79*2*4 #in^2
        self.f_m = 2 #ksi
        self.f_y = 60 #ksi
        

testReinf = testReinf(0,True)
testBlock = testBlock(0)
testElement = testElement(0)

x0, x1, x2, x3, x4, x5, x6 = createPM_masonry(testBlock, testReinf, testElement)

plt.grid(True)
#plot unreduced
plt.plot(x4, x2, color='blue')
#plot reduced
plt.plot(x5, x3, color='red')
plt.plot([0,200,400,600,4500], [x1,x1,x1,x1,x1])
plt.plot([0,100,200,300,3000], [x0,x0,x0,x0,x0])

