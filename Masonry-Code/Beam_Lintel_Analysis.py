# -*- coding: utf-8 -*-
"""
Created on Sun Jun 15 14:14:57 2025

@author: victo
"""
# imports, DO NOT TOUCH!!!--------------------------------------------------------------------
import numpy as np
import sympy as sp
from scipy.linalg import eigh
import matplotlib.pyplot as plt
import math
import pandas as pd
import sys
# imports end --------------------------------------------------------------------------------


# Input requested values as they appear

# is the beam cantalevier or simply suported, surround with ""
# cantalever is, C
# simply supported is SS
Support = "SS"

# for the CMU_Size have "" souround it and use depth x height x length
CMU_Size = "8x8x16"

# mortar type, Options M, S, N, sourround it with ""
mortar_type = "S"

#Grout Pattern, Options bellow, sourround with ""
# Solid units, SU
# Ungrouted Units, UU
# Partial Grouted Units, PGU
# Fully Grouted Units, FGU
Grout_Fill = "PGU"

# number of courses in beam, units number of bricks
Beam_Courses = 15 #bricks

# length of the lintel do not include bearing in the length, use feet for units
Length_Beam = 10 #ft

# bearing length of one side, use inches for units
Length_Bearing = 6 #in

# number of courses above lintel, units is number of bricks
Number_Courses = 10 #bricks


# area based loads

# dead load of the wall, units psf
Dead_load_psf = 50 #psf

# self weight of the beam, units psf
Self_load_psf = 50 #psf

# length based loads 

# dead load of the wall, units plf
Dead_load_plf = 20 #plf

# self weight of the beam, units plf
Self_load_plf = 20 #plf

# live load on the beam, units plf
Live_load_plf = 20 #plf

# roof/floor based live load and dead

# depth of floor that the wall supports, units feet
Floor_depth = 10 #ft

# floor dead load, units psf
Floor_dead_psf = 20 #psf

# floor live load it wont calculate reduction must do by self, units psf
Floor_live_psf = 20 #psf

# point load straight in middle of beam, units of pounds
Point_load = 0 #pounds

# strength of the CMU, units of ksi
f_m = 2 #ksi

# size of horizontal bar, just put the number
bar_size_horizontal = 5

# number of horizontal bars
bar_count_horizontal = 2

# size of vertical bar, just put the number
bar_size_vertical = 5

# vertical spacing, units inches
space = 16 #in

# strength of rebar, units ksi
fy = 60 #ksi

# modulus of Elasticity of steel, units of ksi
E_s = 29000 #ksi

# DO NOT CHANGE ANYTHING FOLLOWING!!!-----------------------------------------------------

Tracker = 0

while Tracker == 0:
    
    # flexure calcs------------------------------------------------------------------------
    
    # splitting CMU Size into Nominal and actual Sizes
    CMU_Size = CMU_Size.lower() # Start of ChatGPT help
    if CMU_Size.count('x') == 2:
        depth_nom, height_nom, length_nom = map(float, CMU_Size.split('x'))
        depth_act, height_act, length_act = [d - 0.375 for d in map(float, CMU_Size.lower().split('x'))] # End of ChatGPT help
    else:
        Tracker = -1
        break
    
    # sizes getting made
    Length = Length_Beam + Length_Bearing/12 #in
    Height_Beam = height_nom * Beam_Courses #in
    Height_Above = height_nom * Number_Courses #in
    
    # finding beam properties
    d = Height_Beam - 2.5 #in
    Sn = depth_act*(Height_Beam**2)/6
    
    # finding area of rebar
    df = pd.read_excel('Masonry_Tables.xlsx', sheet_name='Rebar_Size', engine='openpyxl') # start of ChatGPT helping
    match = df[df["Bar number"] == bar_size_horizontal]
    if not match.empty:
        bar_area_horizontal = match.iloc[0, 2]  # End of ChatGPT helping
    else:
        Tracker = -3
        break
    
    # checking spacing
    S = depth_act-bar_count_horizontal*(2.5)-bar_size_horizontal/8
    if S < 1:
        Tracker = -2
        break
    
    # shape of distributed load
    if Height_Above < Length*12/2 + 8:
        shape = "linear"
    else:
        shape = "triangle"
        
    if Point_load == 0:
        Tracker = 0
    else:
        Tracker = -99
        break
    # add point load dispersion
    #
    #
    #
    #
    
    # finding moment and shear
    Dead_load_klf = (Dead_load_plf + Dead_load_psf*Height_Above/12)/1000 #klf
    Self_load_klf = (Self_load_plf + Self_load_psf*Height_Beam/12)/1000 #klf
    Live_load_klf = Live_load_plf/1000
    Floor_dead_klf = (Floor_dead_psf*Floor_depth)/1000 #klf
    Floor_live_klf = ( Floor_live_psf*Floor_depth)/1000 #klf
    Total_dead_klf = Dead_load_klf + Floor_dead_klf + Self_load_klf #klf
    Total_live_klf = Floor_live_klf + Live_load_klf
    load_combo_1 = 1.4*Total_dead_klf
    load_combo_2 = 1.2*Total_dead_klf + 1.6*Total_live_klf
    if load_combo_1 > load_combo_2:
        w = load_combo_1
    else:
        w = load_combo_2
    Support = Support.upper()
    if Support == "SS":
        if shape == "linear":
            Vu = w*(Length)/2
            Mu = w*(Length**2)/8 #kft
        else:
            Vu = w/2
            Mu = w*Length/6 #kft
    elif Support == "C":
        if shape == "linear":
            Vu = w*Length
            Mu = w*(Length**2)/3 #kft
        else:
            Tracker = -99
            break
    else:
        Tracker = -10
        break
    
    # finding Flexural Strength
    As = bar_area_horizontal*bar_count_horizontal
    Mn = (As*fy*(d-(As*fy/(1.6*f_m*depth_act))))/12 #kft
    
    # checks
    Ey = fy/E_s
    E_min = Ey + 0.003
    c = As*fy/(0.64*f_m*depth_act)
    Es = d*(0.0025/c)-0.0025
    if Es < E_min:
        Tracker = -4
        break
    else:
        phi = 0.9
    phi_Mn = phi*Mn
    if phi_Mn < Mu:
        Tracker = -5
        break
    
    # masonry fr checks
    fr = -1
    types = np.array(["M","S","N"])
    mortar_type = mortar_type.upper()
    for i in range (len(types)):
        if mortar_type == types[i]:
            fr = 0
    if fr == -1:
        Tracker = -6
        break
    grout = np.array(["SU","UU","PGU","FGU"])
    Grout_Fill = Grout_Fill.upper()
    for i in range (len(grout)):
        if Grout_Fill == grout[i]:
            fr = 1
    if fr == 0:
        Tracker = -7
        break
    df = pd.read_excel('Masonry_Tables.xlsx', sheet_name='fr_beam', engine='openpyxl') #start of ChatGPT help
    match = df[df.iloc[:, 0] == Grout_Fill]
    if not match.empty and mortar_type in df.columns:
        fr = match.iloc[0][mortar_type] #end of ChatGPT help
    Mcr = Sn*fr/(12*1000) #kft
    if Mu < Mcr:
        Tracker = -8
        break
    if Mn < 1.3*Mcr:
        Tracker = -9
        break
    
    # Shear Calcs ----------------------------------------------------------------------
    
    SSR = Mu/(Vu*Height_Beam/12)
    if SSR > 1:
        SSR = 1
    Anv = Height_Beam*depth_act
    if SSR < 0.25:
        Vn_max = 6*Anv*(f_m*1000)**(1/2)
    elif SSR == 1:
        Vn_max = 4*Anv*(f_m*1000)**(1/2)
    else:
        Vn_max = 4/3*(5-2*SSR)*Anv*(f_m*1000)**(1/2)
    Vnm = (4-1.75*SSR)*Anv*(f_m*1000)**(1/2)
    phi_v = 0.8
    phi_vnm = phi_v*Vnm
    #phi_vns = Vu - phi_vnm/1000
    #Vns = phi_vns/.8
    #Av_s = Vns/Height_Beam/fy/0.5 # my notes have an additional 1/0.8 but then my answer doesn't match
    #if 0.0007*depth_act > Av_s:
        #Av_s = 0.0007*depth_act
    #Av = Av_s*space
    
    
    # finding area of rebar
    df = pd.read_excel('Masonry_Tables.xlsx', sheet_name='Rebar_Size', engine='openpyxl') # start of ChatGPT helping
    match = df[df["Bar number"] == bar_size_vertical]
    if not match.empty:
        bar_area_vertical = match.iloc[0, 2]  # End of ChatGPT helping
    else:
        Tracker = -11
        break
    Vns = 0.5*(bar_area_vertical/space)*60*1000*Height_Beam
    phi_vns = phi_v*Vns
    V = phi_vns + phi_vnm
    
    # checks
    if Vu*1000 > V:
        Tracker = -12
        break
    if Vn_max < V:
        Tracker = -13
        break
    
    # Deflection--------------------------------------------------------------------------------
    if Length*12 <= 8*d:
        Tracker = 1
        break
    M_cubed = (Mcr/Mu)**3
    In = depth_act*Height_Beam**3/12
    Em = 900*f_m
    n = E_s/Em
    p = As/(depth_act*d)
    kd = d*((p*n)**2+2*p*n)**(1/2)-p*n
    Icr = depth_act*kd**3/3+n*As*(d-kd)**2
    if M_cubed > 0.1:
        I = M_cubed*In+(1-M_cubed)*Icr
    else:
        I = Icr
    if I >In:
        Tracker = -14
        break
    if Support == "SS":
        delta = 5*w*Length**4*12**3/(384*Em*I)
    elif Support == "C":
        delta = w*Length**4*12**3/(8*Em*I)
    delta_allowed = Length*12/600
    if delta > delta_allowed:
        Tracker = -15
        break
    Tracker = 1

# printing
print( )
print( )
print( )
print("Here is the output:")
print( )
# printing any errors
if Tracker == -99:
    print("The code is not desgined to handele this problem it may be due to either point loads being present or a cantilever beam with arching action. I aim to add it soon")
    sys.exit() # chatGPT helped
if Tracker == -1:
    print("The CMU size you inserted is not in the proper form.")
    sys.exit()
if Tracker == -3:
    print("The horizontal bar size is not in the table we use, our table is from 3-11. Sorry for any inconvenence.")
    sys.exit()
if Tracker == -6:
    print("Masonry type you inserted isn't in our list of masonry types.")
    sys.exit()
if Tracker == -7:
    print("Grout fill type you inserted isn't in our list of grout fill types.")
    sys.exit()
if Tracker == -10:
    print("The beam support you inserted is not in our list of supports.")
    sys.exit()
if Tracker == -11:
    print("The vertical bar size is not in the table we use, our table is from 3-11. Sorry for any inconvenence.")
    sys.exit()

# printing all givens
print("Values used:")
print("CMU size in use = " + CMU_Size)
print("CMU nominal:   depth = " + str(depth_nom) + " in        height = " + str(height_nom) + " in        length = " + str(length_nom) + " in")
print("CMU actual:   depth = " + str(depth_act) + " in     height = " + str(height_act) + " in     length = " + str(length_act) + " in")
print("Length of beam = " + str(Length_Beam) + " ft     Bearing Length = " + str(Length_Bearing) + " in")
if Support == "SS":
    print("Beam support type = Simply Supported")
elif Support == "C":
    print("Beam support type = Cantilever")
print("Mortar tyoe in use = " + mortar_type)
if Grout_Fill == "SU":
    print("Grout fill in use = Solid Units")
elif Grout_Fill == "UU":
    print("Grout fill in use = Ungrouted Units")
elif Grout_Fill == "PGU":
    print("Grout fill in use = Partialy Grouted Units")
elif Grout_Fill == "FGU":
    print("Grout fill in use = Fully Grouted Units")
print("CMU Strength = " + str(f_m) + " ksi")
print("Courses of CMU in beam = " + str(Beam_Courses))
print("Size of horizontal reinforcing = #" + str(bar_size_horizontal) + "     Number of horizontal reinforcing = " + str(bar_count_horizontal))
print("Size of vertical reinforcing = #" + str(bar_size_vertical) + "     Spacing of vertical reinforcing = " + str(space) + " in")
print("Rebar Strength = " + str(fy) + " ksi     Rebar Modulus of Elasticity = " + str(E_s) + " ksi")
print("Courses of CMU above beam = " + str(Number_Courses))
print("Area loads applied to beam:   dead = " + str(Dead_load_psf) + " psf     self = " + str(Self_load_psf) + " psf")
print("Length loads applied to beam:   dead = " + str(Dead_load_plf) + " plf     self = " + str(Self_load_plf) + " plf     live = " + str(Live_load_plf) + " plf")
print("Roof/floor depth = " + str(Floor_depth) + " ft")
print("Area loads from roof applied to beam:   dead = " + str(Floor_dead_psf) + " psf     live = " + str(Floor_live_psf) + " psf")
print("Point loads applied to beam = " + str(Point_load) + " lbs")

# printing math
print()
print("Math being done first is flexure")
print("L = L_b + B_l        " + str(Length_Beam) + "+" + str(Length_Bearing) + "/12 = " + str(Length) + " ft")
print("H_b = B_c  h_n        " + str(Beam_Courses) + "*" + str(height_nom) + " = " + str(Height_Beam) + " in")
print("H_a = A_c  h_n        " + str(Number_Courses) + "*" + str(height_nom) + " = " + str(Height_Above) + " in")
print("d = H_b-2.5        " + str(Height_Beam) + "-2.5 = " + str(d) + " in")
print("S_n = {d_b H_b^2}/6        " + "{" + str(depth_act) + "*" + str(Height_Beam) + "^2}/6 = " + str(Sn) + " in^3")
print("Area of 1 horizontal bar = " + str(bar_area_horizontal) + " in^2")
#while to stop running if error is present
Counter = 0
while Counter == 0:
    print("S = d_b-r_nh*2.5-r_dh        " + str(depth_act) + "-" + str(bar_count_horizontal) + "*2.5-" + str(bar_size_horizontal/8) + " = " + str(S) + " in")
    if Tracker == -2:
        print("The spacing for the horizontal rebar is not adequete.")
        print("Therefore the beam is not adequete.")
        Counter = 1
        break
    print("Calculating loading")
    print("D_klf = {D_plf+DS_plf+D_psf*H_a/12+DS_psf*H_b/12+D_Fpsf*d_F}/1000")
    print("{" + str(Dead_load_plf) + "+" + str(Self_load_plf) + "+" + str(Dead_load_psf) + "*" + str(Height_Above) + "/12+" + str(Self_load_psf) + "*" + str(Height_Beam) + "/12+" + str(Floor_dead_psf) + "*" + str(Floor_depth) + "}/1000 = " + str(Total_dead_klf) + " klf")
    print("L_klf = {L_plf+L_Fpsf*d_F}/1000")
    print("{" + str(Live_load_plf) + "+" +str(Floor_live_psf) + "*" + str(Height_Above) + "/12}/1000 = " + str(Total_live_klf) + " klf")
    print("Load Combo 1 = 1.4D        1.4*" + str(Total_dead_klf) + " = " + str(load_combo_1) + " klf")
    print("Load Combo 2 = 1.2D+1.6L        1.2*" + str(Total_dead_klf) + "+1.6*" + str(Total_live_klf) + " = " + str(load_combo_2) + " klf")
    print("We will use " + str(w) + " klf")
    print("Calculating Max Shear and Moment")
    if Support == "SS":
        if shape == "linear":
            print("V_u = {wL}/2        {" + str(w) + "*" + str(Length) + "}/2 = " + str(round(Vu, 3)) + " k")
            print("M_u = {wL^2}/8        {" + str(w) + "*" + str(Length) + "^2}/8 = " + str(round(Mu, 3)) + " kft")
        else:
            print("V_u = w/2        " + str(w) + "/2 = " + str(round(Vu, 3)) + " k")
            print("M_u = {wL}/6        {" + str(w) + "*" + str(Length) + "}/6 = " + str(round(Mu, 3)) + " kft")
    elif Support == "C":
        if shape == "linear":
            print("V_u = wL        " + str(w) + "*" + str(Length) + " = " + str(round(Vu, 3)) + " k")
            print("M_u = {wL^2}/3        {" + str(w) + "*" + str(Length) + "^2}/3 = " + str(round(Mu, 3)) + " kft")
        #else:
            #cantilever arching add here
    print("Finding Flexural Strength")
    print("As = r_ah*r_nh        " + str(bar_area_horizontal) + "*" + str(bar_count_horizontal) + " = " + str(As) + " in^2")
    print("M_n = A_s f_y (d-{A_s f_y}/{1.6f'_m b})")
    print("{" + str(As) + "*" + str(fy) + "(" + str(d) + "-{" + str(As) + "*" + str(fy) + "}/{1.6*" + str(f_m) + "*" + str(depth_act) + "})}/12 = " + str(round(Mn, 3)) + " kft")
    print("Checks")
    print("E_y = f_y/E_s        " + str(fy) + "/" + str(E_s) + " = " + str(round(Ey, 6)))
    print("E_min= E_y + 0.003        " + str(round(Ey, 6)) + "+0.003 = " + str(round(E_min, 6)) +" ")
    print("c = {A_s f_y}/{0.64f'_m b}        {" + str(As) + "*" + str(fy) + "}/{0.64*" + str(f_m) + "*" + str(depth_act) + "} = " + str(round(c, 3)) + " in" )
    print("E_s = d(0.0025/c)-0.0025        " + str(d) + "(0.0025/" + str(round(c, 3)) + ")-0.0025 = " + str(round(Es, 6)))
    if Tracker == -4:
        print("E_s > E_min,        X    rather        " + str(round(Es, 6)) + "<" + str(round(E_min, 6)))
        print("E_min: is larger than E_s and as it stand the code can not handle that so the rest will")
        print("need to be done by hand, sorry for any inconvienence.")
        print("Therefore the beam is not adequete.")
        Counter = 1
        break
    print("E_s > E_min,        " + str(round(Es, 6)) + ">" + str(round(E_min, 6)) + " GOOD")
    print("Φ = 0.9")
    print("ΦM_n = " + str(phi) + "*" + str(round(Mn, 3)) + " = " + str(round(phi_Mn, 3)) + " kft")
    if Tracker == -5:
        print("ΦM_n > M_u        X    rather        " + str(round(phi_Mn, 3)) + "<" + str(round(Mu, 3)))
        print("M_u  is larger than ΦM_n  which is against code.")
        print("Therefore the beam is not adequete.")
        Counter = 1
        break
    print("ΦM_n > M_u        " + str(round(phi_Mn, 3)) + ">" + str(round(Mu, 3)) + " GOOD")
    print("F_r = " + str(fr) + " psi")
    print("M_cr = {S_n f_r}/{12*1000}        {" + str(Sn) + "*" + str(fr) + "}/{12*1000} = " + str(Mcr) + " kft")
    if Tracker == -8:
        print("M_u > M_cr        X    rather        " + str(round(Mu, 3)) + "<" + str(round(Mcr, 3)))
        print("M_cr  is larger than M_u  which is against code.")
        print("Therefore the beam is not adequete.")
        Counter = 1
        break
    print("M_u > M_cr        " + str(round(Mu, 3)) + ">" + str(round(Mcr, 3)) + " GOOD")
    if Tracker == -9:
        print("M_n > 1.3M_cr        X    rather        " + str(round(Mn, 3)) + "<" + str(round(1.3*Mcr, 3)))
        print("1.3M_cr  is larger than M_n  which is against code.")
        print("Therefore the beam is not adequete.")
        Counter = 1
        break
    print("M_n > 1.3M_cr        " + str(round(Mn, 3)) + ">" + str(round(1.3*Mcr, 3)) + " GOOD")
    print("Shear calculations.")
    print("SSR = M_u/{V_u*H_b/12}        " + str(round(Mu, 3)) + "/{" + str(round(Vu, 3)) + "*" + str(Height_Beam) + "/12} = " + str(Mu/(Vu*Height_Beam/12)))
    if Mu/(Vu*Height_Beam/12) > 1:
        print("Since SSR is larger than 1 we just use SSR as 1.")
    print("A_nv = H_b b        " + str(Height_Beam) + "*" + str(depth_act) + " = " + str(Anv) + " in^2")
    if SSR < 0.25:
        print("V_{n-max} = 6A_nv (f'_m*1000)^(1/2)        6*" + str(Anv) + "√(" + str(f_m) + "*1000) = " + str(round(Vn_max, 3)) + " lbs")
    elif SSR == 1:
        print("V_{n-max} = 4A_nv √(f'_m*1000)        4*" + str(Anv) + "(" + str(f_m) + "*1000)^(1/2) = " + str(round(Vn_max, 3)) + " lbs")
    else:
        print("V_{n-max} = 4/3 (5-2SSR)A_nv √(f'_m*1000)        4/3 (5-2*" + str(round(SSR, 3)) + ")" + str(Anv) + "√(" + str(f_m) + "*1000) = " + str(round(Vn_max, 3)) + " lbs")
    print("V_nm = (4-1.75SSR)A_nv √(f'_m*1000)        (4-1.75*" + str(round(SSR, 3)) + ")" + str(Anv) + "√(" + str(f_m) + "*1000) = " + str(round(Vnm, 3)) + " lbs")
    print("Φ_v = 0.8")
    print("Φ_v V_nm = " + str(phi_v) + "*" + str(round(Vnm, 3)) + " = " + str(round(phi_vnm, 3)))
    print("Vertical bar area = " + str(bar_area_vertical) + " in^2")
    print("V_ns = 0.5(A_vb/space)60*1000*H_b        0.5(" + str(bar_area_vertical) + "/" + str(space) + ")*60*1000*" + str(Height_Beam) + " = " + str(round(Vns, 3)) + " lbs")    
    print("Φ_v V_ns = " + str(phi_v) + "*" + str(round(Vns, 3)) + " = " + str(round(phi_vns, 3)) + " lbs")    
    print("V = Φ_v V_ns + Φ_v V_nm        " + str(round(phi_vns, 3)) + "*" + str(round(phi_vnm, 3)) + " = " + str(round(V, 3)) + " lbs")
    if Tracker == -12:
        print("V > V_u        X    rather        " + str(round(V, 3)) + "<" + str(round(Vu*1000, 3)))
        print("V_u  is larger than V  which is against code.")
        print("Therefore the beam is not adequete.")
        Counter = 1
        break
    print("V > V_u        " + str(round(V, 3)) + ">" + str(round(Vu*1000, 3)) + " GOOD")
    if Tracker == -13:
        print("V_{n-max} > V        X    rather        " + str(round(Vn_max, 3)) + "<" + str(round(V, 3)))
        print("V  is larger than V_{n-max}  which is against code.")
        print("Therefore the beam is not adequete.")
        Counter = 1
        break
    print("V_{n-max} > V        " + str(round(Vn_max, 3)) + ">" + str(round(V, 3)) + " GOOD")
    print("Deflection Calculations.")
    if Length*12 <= 8*d:
        print("L*12<=8d        " + str(Length) + "*12<=8*" + str(d) + "        "+ str(Length*12) + "<=" + str(8*d))
        print("Therefore we don't need to check deflection.")
        Counter = 1
        break
    print("L*12<=8d        " + str(Length) + "*12<=8*" + str(d) + "        "+ str(Length*12) + "<=" + str(8*d) + "     NOPE")
    print("Therefore we need to check deflection.")
    print("M^3 = (Mcr/Mu)^3        (" + str(round(Mcr, 3)) + "/" + str(round(Mu, 3)) + ")^3 = " + str(round(M_cubed, 3)))
    print("I_n = {bH_b^3}/12        {" + str(depth_act) + "*" + str(Height_Beam) + "^3}/12 = " + str(In) + " in^4")
    print("Em = 900f'_m        900*" + str(f_m) + " = " + str(Em) + " ksi")
    print("n = Es/Em        " + str(E_s) +"/" + str(Em) + " = " + str(round(n, 3)))
    print("p = A_s/(bd)        " + str(As) + "/(" + str(depth_act) + "*" + str(d) + ") = " + str(round(p, 6)))
    print("kd = d√((pn)^2+2pn)-pn")
    print(str(depth_act) + "√((" + str(round(p, 6)) + "*" + str(round(n, 3)) + ")^2+2*" + str(round(p, 6)) + "*" + str(round(n, 3)) + ")-" + str(round(p, 6)) + "*" + str(round(n, 3)) + " = " + str(round(kd, 3)))
    print("I_cr = {bkd^3}/3+nA_s (d-kd)^2")
    print("{" +str(depth_act) + "*" + str(round(kd, 3)) + "^3}/3+" + str(round(n, 3)) + "*" + str(As) + "(" + str(depth_act) + "-" + str(round(kd, 3)) + ")^2 = " + str(round(Icr, 3)) + " in^4")
    if M_cubed > 0.1:
        print("I = M^3 I_n+(1-M^3)I_cr        " + str(round(M_cubed, 3)) + "*" + str(In) + "+(1-" + str(round(M_cubed, 3)) + ")" + str(round(Icr, 3)) + " = " + str(round(I, 3))+ " in^4")
    else:
        print("I = I_cr = " + str(round(Icr, 3)) + " in^4" )
    if Tracker == -14:
        print("I_n > I        X    rather        " + str(round(In, 3)) + "<" + str(round(I, 3)))
        print("I  is larger than I_n  which is against code and logic since the cracked area shouldn't be larger than the starting area.")
        print("Therefore the beam is not adequete.")
        Counter = 1
        break
    print("I_n > I        " + str(round(In, 3)) + ">" + str(round(I, 3)))
    if Support == "SS":
        print("Δ = {5wL^4*12^3}/(384EI)        {5*" + str(w) + "*" + str(Length) + "^4*12^3}/(384*" + str(Em) + "*" + str(round(Icr, 3)) + ") = " + str(round(delta, 3)) + " in")
    elif Support == "C":
        print("Δ = {wL^4*12^3}/(8EI)        {" + str(w) + "*" + str(Length) + "^4*12^3}/(8*" + str(Em) + "*" + str(round(Icr, 3)) + ") = " + str(round(delta, 3)) + " in")
    delta_allowed = Length*12/600
    if delta > delta_allowed:
        Tracker = -15
        break
    print("Δ_allowed = {L*12}/600        {" + str(Length) + "*12}/600 = " + str(round(delta_allowed, 3)) + " in")
    if Tracker == -15:
        print("Δ_allowed > Δ        X    rather        " + str(round(delta_allowed, 3)) + "<" + str(round(delta, 3)))
        print("Δ  is larger than Δ_allowed  which is against code.")
        print("Therefore the beam is not adequete.")
        Counter = 1
        break
    print("Δ_allowed > Δ        " + str(round(delta_allowed, 3)) + ">" + str(round(delta, 3)))
    print("The beam is adequete.")
    Counter = 1

