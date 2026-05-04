# -*- coding: utf-8 -*-
"""
Created on Wed Aug 13 10:45:00 2025

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
from MasonryColumnBase import Block
# imports end --------------------------------------------------------------------------------


# Input requested values as they appear

# is the beam cantalevier or simply suported, surround with ""
# cantalever is, C
# simply supported is SS
Support = "SS"

# plug in the CMU size you want to try
# for the CMU_Size have "" souround it and use depth x height x length
CMU_Size = "8x8x16"

# mortar type, Options M, S, N, sourround it with ""
mortar_type = "S"

#Grout Pattern, Options bellow, sourround with ""
# Solid units, SU
# Ungrouted Units, UU
# Partial Grouted Units, PGU
# Fully Grouted Units, FGU
Grout_Fill = "FGU"

# number of courses from bottom to top
Courses = 15 #bricks

# length of the lintel do not include bearing in the length, use feet for units
Length_Beam = 10 #ft

# bearing length of one side, use inches for units
Length_Bearing = 6 #in

# area based loads

# dead load of the wall, units psf
Dead_load_psf = 50 #psf

# self weight of the beam, units psf
Self_load_psf = 50 #psf

# length based loads 

# dead load of the wall, units plf
Dead_load_plf = 100 #plf

# self weight of the beam, units plf
Self_load_plf = 100 #plf

# live load on the beam, units plf
Live_load_plf = 100 #plf

# roof/floor based live load and dead

# depth of floor that the wall supports, units feet
Floor_depth = 10 #ft

# floor dead load, units psf
Floor_dead_psf = 100 #psf

# floor live load it wont calculate reduction must do by self, units psf
Floor_live_psf = 50 #psf

# point load straight in middle of beam, units of pounds
Point_load = 0 #pounds

# strength of the CMU, units of ksi
f_m = 2 #ksi

# strength of rebar, units ksi
fy = 50 #ksi

# modulus of Elasticity of steel, units of ksi
E_s = 29000 #ksi

# distance you want the rebar from the face of The CMU Code specifies minimum, suggested is 2.5 units in
gap = 2.5 # in

# vertical spacing, units inches
space = 24 #in


# DO NOT CHANGE ANYTHING FOLLOWING!!!-----------------------------------------------------

fr = -1
types = np.array(["M","S","N"])
mortar_type = mortar_type.upper()
for i in range (len(types)):
    if mortar_type == types[i]:
        fr = 0
if fr == -1:
    print("The mortar type inserted is not in the code we only handle M, S, N types.")
    sys.exit()
grout = np.array(["SU","UU","PGU","FGU"])
Grout_Fill = Grout_Fill.upper()
for i in range (len(grout)):
    if Grout_Fill == grout[i]:
        fr = 1
if fr == 0:
    print("The grout type inserted is not in the code we only handle SU, UU, PGU, FGU types.")
    sys.exit()
    
# splitting CMU into parts
if CMU_Size.count('x') == 2:
    depth_nom, height_nom, length_nom = map(float, CMU_Size.split('x'))
    depth_act, height_act, length_act = [d - 0.375 for d in map(float, CMU_Size.lower().split('x'))]
    
# sizes getting made
Length = Length_Beam + Length_Bearing/12 #in
Length = (round(Length, 3))

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
print("Rebar Strength = " + str(fy) + " ksi     Rebar Modulus of Elasticity = " + str(E_s) + " ksi")
print("Area loads applied to beam:   dead = " + str(Dead_load_psf) + " psf     self = " + str(Self_load_psf) + " psf")
print("Length loads applied to beam:   dead = " + str(Dead_load_plf) + " plf     self = " + str(Self_load_plf) + " plf     live = " + str(Live_load_plf) + " plf")
print("Roof/floor depth = " + str(Floor_depth) + " ft")
print("Area loads from roof applied to beam:   dead = " + str(Floor_dead_psf) + " psf     live = " + str(Floor_live_psf) + " psf")
print("Point loads applied to beam = " + str(Point_load) + " lbs")
# printing math
print()
print("Math being done first is flexure")
print("L = L_b + B_l        " + str(Length_Beam) + "+" + str(Length_Bearing) + "/12 = " + str(Length) + " ft")

Beam_Courses = 1
count1 = 0
while count1 == 0:
    Beam_Courses += 1
    if Courses < Beam_Courses:
        print("There is no possible beam that works from the given information.")
        sys.exit()
    print("Trying " + str(Beam_Courses) + " beam courses.")
    Number_Courses = Courses - Beam_Courses
    print( "C_a = " + str(Courses) + "-" + str(Beam_Courses) + " = " + str(Number_Courses))
    Height_Beam = height_nom * Beam_Courses #in
    print("H_b = B_c  h_n        " + str(Beam_Courses) + "*" + str(height_nom) + " = " + str(Height_Beam) + " in")
    Height_Above = height_nom * Number_Courses
    print("H_a = C_a  h_n        " + str(Number_Courses) + "*" + str(height_nom) + " = " + str(Height_Above) + " in")
    bar_size_horizontal = 2
    count2 = 0
    while count2 == 0:
        bar_size_horizontal += 1
        if bar_size_horizontal > 11:
            count2 = -1
            break
        print("Trying size " + str(bar_size_horizontal) + " rebar for horizontal.")
        # finding properties of rebar
        df = pd.read_excel('Masonry_Tables.xlsx', sheet_name='Rebar_Size', engine='openpyxl') # start of ChatGPT helping
        match = df[df["Bar number"] == bar_size_horizontal]
        if not match.empty:
            bar_area_horizontal = match.iloc[0, 2]  # End of ChatGPT helping
        if not match.empty:
            bar_dia_horizontal = match.iloc[0, 1]  # End of ChatGPT helping
        print("Rebar area = " + str(bar_area_horizontal) + " in^2")
        print("Rebar diameter = " + str(bar_dia_horizontal) + " in")    
        bar_count_horizontal = 1
        count3 = 0
        while count3 == 0:
            bar_count_horizontal += 1
            print("Trying  " + str(bar_count_horizontal) + " horizontal rebars.")
            S = depth_act-2*(gap)-(bar_count_horizontal-1)*(bar_dia_horizontal)
            print("S = d_b-2*gap-(r_nh-1)(r_dh)        " + str(depth_act) + "-2*" +str(gap) + "-(" + str(bar_count_horizontal) + "-1)(" + str(bar_dia_horizontal) + ") = " + str(S) + " in")
            if 1 > bar_dia_horizontal:
                S_check = 1
            else:
                S_check = bar_dia_horizontal
            if S < S_check:
                print("S > S check       X rather       S < S check     " + str(S) + " < " +  str(S_check))
                count3 = -1
                break
            print("S > S check       " + str(S) + " > " +  str(S_check))
            
            d = Height_Beam - gap #in
            print("d = H_b-gap        " + str(Height_Beam) + str(gap) + " = " + str(d) + " in")
            Sn = depth_act*(Height_Beam**2)/6
            Sn = (round(Sn,3))
            print("S_n = {d_b H_b^2}/6        " + "{" + str(depth_act) + "*" + str(Height_Beam) + "^2}/6 = " + str(Sn) + " in^3")
            As = bar_area_horizontal*bar_count_horizontal
            print("As = r_ah*r_nh        " + str(bar_area_horizontal) + "*" + str(bar_count_horizontal) + " = " + str(As) + "in^2")
            # shape of distributed load
            if Height_Above < Length*12/2 + 8:
                shape = "linear"
                print("H_a < L       " + str(Height_Above) + " < " + str(Length) + " This means it is linear.")
            else:
                shape = "triangle"
                print("H_a > L       " + str(Height_Above) + " > " + str(Length) + " This means it has arching.")
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
            
            # Calculating loading
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
            print("Calculating loading")
            print("D_klf = {D_plf+DS_plf+D_psf*H_a/12+DS_psf*H_b/12+D_Fpsf*d_F}/1000")
            print("{" + str(Dead_load_plf) + "+" + str(Self_load_plf) + "+" + str(Dead_load_psf) + "*" + str(Height_Above) + "/12+" + str(Self_load_psf) + "*" + str(Height_Beam) + "/12+" + str(Floor_dead_psf) + "*" + str(Floor_depth) + "}/1000 = " + str(Total_dead_klf) + " klf")
            print("L_klf = {L_plf+L_Fpsf*d_F}/1000")
            print("{" + str(Live_load_plf) + "+" +str(Floor_live_psf) + "*" + str(Height_Above) + "/12}/1000 = " + str(Total_live_klf) + " klf")
            print("Load Combo 1 = 1.4D        1.4*" + str(Total_dead_klf) + " = " + str(load_combo_1) + " klf")
            print("Load Combo 2 = 1.2D+1.6L        1.2*" + str(Total_dead_klf) + "+1.6*" + str(Total_live_klf) + " = " + str(load_combo_2) + " klf")
            print("We will use " + str(w) + " klf")
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
                    sys.exit()
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
                    
            # finding Flexural Strength
            Mn = (As*fy*(d-(As*fy/(1.6*f_m*depth_act))))/12 #kft
            print("M_n = A_s f_y (d-{A_s f_y}/{1.6f'_m b})")
            print("{" + str(As) + "*" + str(fy) + "(" + str(d) + "-{" + str(As) + "*" + str(fy) + "}/{1.6*" + str(f_m) + "*" + str(depth_act) + "})}/12 = " + str(round(Mn, 3)) + " kft")
            
            print("Checks")
            Ey = fy/E_s
            print("E_y = f_y/E_s        " + str(fy) + "/" + str(E_s) + " = " + str(round(Ey, 6)))
            E_min = Ey + 0.003
            print("E_min= E_y + 0.003        " + str(round(Ey, 6)) + "+0.003 = " + str(round(E_min, 6)) +" ")
            c = As*fy/(0.64*f_m*depth_act)
            print("c = {A_s f_y}/{0.64f'_m b}        {" + str(As) + "*" + str(fy) + "}/{0.64*" + str(f_m) + "*" + str(depth_act) + "} = " + str(round(c, 3)) + " in" )
            Es = d*(0.0025/c)-0.0025
            print("E_s = d(0.0025/c)-0.0025        " + str(d) + "(0.0025/" + str(round(c, 3)) + ")-0.0025 = " + str(round(Es, 6)))
            if Es < E_min:
                print("E_s > E_min,        X    rather        " + str(round(Es, 6)) + "<" + str(round(E_min, 6)))
                continue  # ChatGPT helped
            else:
                print("E_s > E_min,        " + str(round(Es, 6)) + ">" + str(round(E_min, 6)) + " GOOD")
                phi = 0.9
                print("Φ = 0.9")
            phi_Mn = phi*Mn
            print("ΦM_n = " + str(phi) + "*" + str(round(Mn, 3)) + " = " + str(round(phi_Mn, 3)) + " kft")
            if phi_Mn < Mu:
                print("ΦM_n > M_u        X    rather        " + str(round(phi_Mn, 3)) + "<" + str(round(Mu, 3)))
                continue
            else:
                print("ΦM_n > M_u        " + str(round(phi_Mn, 3)) + ">" + str(round(Mu, 3)) + " GOOD")
           #fr part of check
            df = pd.read_excel('Masonry_Tables.xlsx', sheet_name='fr_beam', engine='openpyxl') #start of ChatGPT help
            match = df[df.iloc[:, 0] == Grout_Fill]
            if not match.empty and mortar_type in df.columns:
                fr = match.iloc[0][mortar_type] #end of ChatGPT help
            Mcr = Sn*fr/(12*1000) #kft
            print("F_r = " + str(fr) + " psi")
            print("M_cr = {S_n f_r}/{12*1000}        {" + str(Sn) + "*" + str(fr) + "}/{12*1000} = " + str(Mcr) + " kft")
            if Mu < Mcr:
                print("M_u > M_cr        X    rather        " + str(round(Mu, 3)) + "<" + str(round(Mcr, 3)))
                continue
            else:
                print("M_u > M_cr        " + str(round(Mu, 3)) + ">" + str(round(Mcr, 3)) + " GOOD")
            if Mn < 1.3*Mcr:
                print("M_n > 1.3M_cr        X    rather        " + str(round(Mn, 3)) + "<" + str(round(1.3*Mcr, 3)))
                continue
            else:
                print("M_n > 1.3M_cr        " + str(round(Mn, 3)) + ">" + str(round(1.3*Mcr, 3)) + " GOOD")
            #deflection calcs
            print("Deflection Calculations.")
            if Length*12 <= 8*d:
                print("L*12<=8d        " + str(Length) + "*12<=8*" + str(d) + "        "+ str(Length*12) + "<=" + str(8*d))
                print("Therefore we don't need to check deflection.")
            else:
                print("L*12<=8d        " + str(Length) + "*12<=8*" + str(d) + "        "+ str(Length*12) + "<=" + str(8*d) + "     NOPE")
                print("Therefore we need to check deflection.")
                M_cubed = (Mcr/Mu)**3
                print("M^3 = (Mcr/Mu)^3        (" + str(round(Mcr, 3)) + "/" + str(round(Mu, 3)) + ")^3 = " + str(round(M_cubed, 3)))
                In = depth_act*Height_Beam**3/12
                print("I_n = {bH_b^3}/12        {" + str(depth_act) + "*" + str(Height_Beam) + "^3}/12 = " + str(In) + " in^4")
                Em = 900*f_m
                print("Em = 900f'_m        900*" + str(f_m) + " = " + str(Em) + " ksi")
                n = E_s/Em
                print("n = Es/Em        " + str(E_s) +"/" + str(Em) + " = " + str(round(n, 3)))
                p = As/(depth_act*d)
                print("p = A_s/(bd)        " + str(As) + "/(" + str(depth_act) + "*" + str(d) + ") = " + str(round(p, 6)))
                kd = d*((p*n)**2+2*p*n)**(1/2)-p*n
                print("kd = d√((pn)^2+2pn)-pn")
                print(str(depth_act) + "√((" + str(round(p, 6)) + "*" + str(round(n, 3)) + ")^2+2*" + str(round(p, 6)) + "*" + str(round(n, 3)) + ")-" + str(round(p, 6)) + "*" + str(round(n, 3)) + " = " + str(round(kd, 3)))
                Icr = depth_act*kd**3/3+n*As*(d-kd)**2
                print("I_cr = {bkd^3}/3+nA_s (d-kd)^2")
                print("{" +str(depth_act) + "*" + str(round(kd, 3)) + "^3}/3+" + str(round(n, 3)) + "*" + str(As) + "(" + str(depth_act) + "-" + str(round(kd, 3)) + ")^2 = " + str(round(Icr, 3)) + " in^4")
                if M_cubed > 0.1:
                    I = M_cubed*In+(1-M_cubed)*Icr
                    print("I = M^3 I_n+(1-M^3)I_cr        " + str(round(M_cubed, 3)) + "*" + str(In) + "+(1-" + str(round(M_cubed, 3)) + ")" + str(round(Icr, 3)) + " = " + str(round(I, 3))+ " in^4")
                else:
                    I = Icr
                    print("I = I_cr = " + str(round(Icr, 3)) + " in^4" )
                if I >In:
                    print("I_n > I        X    rather        " + str(round(In, 3)) + "<" + str(round(I, 3)))
                    continue
                else:
                    print("I_n > I        " + str(round(In, 3)) + ">" + str(round(I, 3)))
                if Support == "SS":
                    delta = 5*w*Length**4*12**3/(384*Em*I)
                    print("Δ = {5wL^4*12^3}/(384EI)        {5*" + str(w) + "*" + str(Length) + "^4*12^3}/(384*" + str(Em) + "*" + str(round(Icr, 3)) + ") = " + str(round(delta, 3)) + " in")
                elif Support == "C":
                    delta = w*Length**4*12**3/(8*Em*I)
                    print("Δ = {wL^4*12^3}/(8EI)        {" + str(w) + "*" + str(Length) + "^4*12^3}/(8*" + str(Em) + "*" + str(round(Icr, 3)) + ") = " + str(round(delta, 3)) + " in")
                delta_allowed = Length*12/600
                print("Δ_allowed = {L*12}/600        {" + str(Length) + "*12}/600 = " + str(round(delta_allowed, 3)) + " in")
                if delta > delta_allowed:
                    print("Δ_allowed > Δ        X    rather        " + str(round(delta_allowed, 3)) + "<" + str(round(delta, 3)))
                    continue
                else:
                    print("Δ_allowed > Δ        " + str(round(delta_allowed, 3)) + ">" + str(round(delta, 3)))
            # Shear Calcs
            print("Shear calculations.")
            SSR = Mu/(Vu*Height_Beam/12)
            print("SSR = M_u/{V_u*H_b/12}        " + str(round(Mu, 3)) + "/{" + str(round(Vu, 3)) + "*" + str(Height_Beam) + "/12} = " + str(Mu/(Vu*Height_Beam/12)))
            if SSR > 1:
                SSR = 1
                print("Since SSR is larger than 1 we just use SSR as 1.")
            Anv = Height_Beam*depth_act
            print("A_nv = H_b b        " + str(Height_Beam) + "*" + str(depth_act) + " = " + str(Anv) + " in^2")
            if SSR < 0.25:
                Vn_max = 6*Anv*(f_m*1000)**(1/2)
                print("V_{n-max} = 6A_nv (f'_m*1000)^(1/2)        6*" + str(Anv) + "√(" + str(f_m) + "*1000) = " + str(round(Vn_max, 3)) + " lbs")
            elif SSR == 1:
                Vn_max = 4*Anv*(f_m*1000)**(1/2)
                print("V_{n-max} = 4A_nv √(f'_m*1000)        4*" + str(Anv) + "(" + str(f_m) + "*1000)^(1/2) = " + str(round(Vn_max, 3)) + " lbs")
            else:
                Vn_max = 4/3*(5-2*SSR)*Anv*(f_m*1000)**(1/2)
                print("V_{n-max} = 4/3 (5-2SSR)A_nv √(f'_m*1000)        4/3 (5-2*" + str(round(SSR, 3)) + ")" + str(Anv) + "√(" + str(f_m) + "*1000) = " + str(round(Vn_max, 3)) + " lbs")
            Vnm = (4-1.75*SSR)*Anv*(f_m*1000)**(1/2)
            print("V_nm = (4-1.75SSR)A_nv √(f'_m*1000)        (4-1.75*" + str(round(SSR, 3)) + ")" + str(Anv) + "√(" + str(f_m) + "*1000) = " + str(round(Vnm, 3)) + " lbs")
            phi_v = 0.8
            print("Φ_v = 0.8")
            phi_vnm = phi_v*Vnm
            print("Φ_v V_nm = " + str(phi_v) + "*" + str(round(Vnm, 3)) + " = " + str(round(phi_vnm, 3)))
            if phi_vnm > Vu:
                print("ΦVnm > Vu     " + str(phi_vnm) + ">" + str(Vu) + "     Therefore no vertical rebar needed.")
                print("")
                print("Values we are using:")
                print("CMU Size is " + CMU_Size)
                print("Mortar type is " + mortar_type)
                print("Grout fill is " + Grout_Fill)
                print("Beam Courses is " + str(Beam_Courses))
                print("Horizontal rebar size is " + str(bar_size_horizontal))
                print("Number of horizontal rebar " + str(bar_count_horizontal))
                print("No horizontal rebar required.")
            bar_size_vertical = 2
            count4 = 0
            while count4 == 0:
                bar_size_vertical += 1
                print("Trying  " + str(bar_size_vertical) + " horizontal rebars.")
                # finding area of rebar
                df = pd.read_excel('Masonry_Tables.xlsx', sheet_name='Rebar_Size', engine='openpyxl') # start of ChatGPT helping
                match = df[df["Bar number"] == bar_size_vertical]
                if not match.empty:
                    bar_area_vertical = match.iloc[0, 2]
                    print("Vertical bar area = " + str(bar_area_vertical) + " in^2")
                else:
                    print("There is no shear reinforcement that works from the given information.")
                    sys.exit()
                    break
                Vns = 0.5*(bar_area_vertical/space)*60*1000*Height_Beam
                print("V_ns = 0.5(A_vb/space)60*1000*H_b        0.5(" + str(bar_area_vertical) + "/" + str(space) + ")*60*1000*" + str(Height_Beam) + " = " + str(round(Vns, 3)) + " lbs")
                phi_vns = phi_v*Vns
                print("Φ_v V_ns = " + str(phi_v) + "*" + str(round(Vns, 3)) + " = " + str(round(phi_vns, 3)) + " lbs")    
                V = phi_vns + phi_vnm
                print("V = Φ_v V_ns + Φ_v V_nm        " + str(round(phi_vns, 3)) + "*" + str(round(phi_vnm, 3)) + " = " + str(round(V, 3)) + " lbs")
                # checks
                if Vu*1000 > V:
                    print("V > V_u        X    rather        " + str(round(V, 3)) + "<" + str(round(Vu*1000, 3)))
                    continue
                else:
                    print("V > V_u        " + str(round(V, 3)) + ">" + str(round(Vu*1000, 3)) + " GOOD")
                if Vn_max < V:
                    print("V_{n-max} > V        X    rather        " + str(round(Vn_max, 3)) + "<" + str(round(V, 3)))
                    continue
                else:
                    print("V_{n-max} > V        " + str(round(Vn_max, 3)) + ">" + str(round(V, 3)) + " GOOD")
                    V_eq = Vu-phi_vnm/1000
                    distance = V_eq/w
                    bar_count_vertical = round((distance/(space/12))+0.5,0)
                    print(str(Vu) + "-" + str(phi_vnm/1000) + " = " + str(V_eq))
                    print(str(V_eq) + "/" + str(w) + " = " + str(distance)) 
                    print(str(distance) + "/(" + str(space) + "/12) = " + str(distance/(space/12)))
                    print("Rounded number of vertical bars = " + str(bar_count_vertical))
                    
                    print("")
                    print("Values we are using:")
                    print("CMU Size is " + CMU_Size)
                    print("Mortar type is " + mortar_type)
                    print("Grout fill is " + Grout_Fill)
                    print("Beam Courses is " + str(Beam_Courses))
                    print("Horizontal rebar size is " + str(bar_size_horizontal))
                    print("Number of horizontal rebar " + str(bar_count_horizontal))
                    print("Vertical rebar size is " + str(bar_size_vertical))
                    print("Spacing between vertical rebar " + str(space) + " in")
                    sys.exit()
            
            
            
                
            
            
            

           

            
                    














