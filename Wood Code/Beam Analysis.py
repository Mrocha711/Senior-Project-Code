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

# What is the size of the wood being used, examples 2x2, 4x4 and so on. You need "" around the word.
size = "2x12"

# What speices are you using, these appear as they are in the NDS, so if the NDS has 
# multiple names it is required. Must have "" around it.
speices = "Douglas Fir-Larch, Douglas Fir, Western Larch"

# What grade is it. If it is dense, must be first word, for Number do No tehn number no space.
# Examples Select Structural, No1, Dense No2. Must use "" around it also capitilize first letter of each word
grade = "No1"

# load durartion, from list pick highest value that applies as is worse case senario. Use "" around it.
# Permanent
# Live
# Snow
# Construction
# Wind/Eq
# Impact
load_dur = "Live"

# Is the Mouister content when in use exceeding 19%. Either True or False
Mouister = False

# Is the tempreatue exceding 100 F. Either True or False
T100 = False

# Is the tempreatue exceding 125 F. Either True or False
T125 = False

# Is the wood incised. Either True or False
incised = False

# Is the member repetitive meaning similare members are within 24" of it. Either True or False
repetitive = False

#length from one support to another support in ft, if diffrent sizees use longest span.
length = 20

#Total length of the beam in ft
length_total = 20

# What is its support condition need "" around
# Options cantilever or simply supported
Support = "simply supported"

# load that is applied. Need "" around.
# for cantilever options: Uniformly Distributed, Concentrated load at end
# for simply supported: Uniformly Distributed, Concentrated load at center,
# 2 Concentrated loads even with support, 3 Concentrated loads even with support,
# 4 Concentrated loads even with support, 5 Concentrated loads even with support,
# 6 Concentrated loads even with support, 7 Concentrated loads even with support,
# Equal End moments
# Other is for any note stated, also include point loads not evenly spaced.
load = "Concentrated load at center"

# is member supported latteraly according to code. Check 4.41 in NDS for code requirements
# True or false
Lateral = False

# Is the Compression side braced its full length, example plywood on a roof.
braced = False

# The Max moment the beam experiences in pft
M_max = 3000

# The Max shear the beam experiences in p
V_max = 600

# The allowable deflection the beam experiences in in
Δ_allow = 1

# The deflection still mising division by E and I, the beam experiences in in, you can write it as an EQ
Δ_EI = 5*60*20**4*12**3/(384)

#DO NOT TOUCH CODE

# length check
if length > length_total:
    print("The length between two supports is longer than the whole beams length please double check that you entered the right values in the proper place.")
    sys.exit()

# table of values
Values = np.ones((7,12))

#Grabbing all info
size = size.lower()
df = pd.read_excel('Wood_tables.xlsx', sheet_name='Size Properties ', engine='openpyxl') 
match = df[df["Name"] == size]
if not match.empty:
    match_np = match.to_numpy() # ChatGpt assisted
    b_nom = match_np[0, 1]
    d_nom = match_np[0, 2]
    b_act = match_np[0, 3]
    d_act = match_np[0, 4]
    A = match_np[0, 5]
    Sxx = match_np[0, 6]
    Ixx = match_np[0, 7]
    Syy = match_np[0, 8]
    Iyy = match_np[0, 9]
    Size_Name = match_np[0, 10]
    my_class = match_np[0, 11]
else:
    print("The size you gave is not in our list of sizes please double check you have entered it right.")
    sys.exit()

#Finding all vales for adjustments
speices = speices.lower()
Ref_values = my_class + " Ref Values"
df = pd.read_excel('Wood_tables.xlsx', sheet_name= Ref_values, engine='openpyxl') 
match = df[df["Species"] == speices]

if not match.empty:
    final_match = match[match['Grade'] == grade] # ChatGPT assisted
    if not final_match.empty:
        final_match_np = final_match.to_numpy()
        if my_class == "Small":
            if "2+" == final_match_np[0, 2]:
                Values[0,0] = final_match_np[0, 3]
                Values[1,0] = final_match_np[0, 4]
                Values[2,0] = final_match_np[0, 5]
                Values[3,0] = final_match_np[0, 6]
                Values[4,0] = final_match_np[0, 7]
                Values[5,0] = final_match_np[0, 8]
                Values[6,0] = final_match_np[0, 9]
            else:
                if d_nom <= 4:
                    Values[0,0] = final_match_np[0, 3]
                    Values[1,0] = final_match_np[0, 4]
                    Values[2,0] = final_match_np[0, 5]
                    Values[3,0] = final_match_np[0, 6]
                    Values[4,0] = final_match_np[0, 7]
                    Values[5,0] = final_match_np[0, 8]
                    Values[6,0] = final_match_np[0, 9]
                else:
                    print("The size and grade ar not compatible, for your grade the max size is 4.")
        else:
            final_match = match[match['Size'] == Size_Name]
            if not final_match.empty:
                final_match_np = final_match.to_numpy()
            Values[0,0] = final_match_np[0, 3]
            Values[1,0] = final_match_np[0, 4]
            Values[2,0] = final_match_np[0, 5]
            Values[3,0] = final_match_np[0, 6]
            Values[4,0] = final_match_np[0, 7]
            Values[5,0] = final_match_np[0, 8]
            Values[6,0] = final_match_np[0, 9]
    else:
        print("The grade you gave is not in our list of grades for that speices please double check you have entered it right.")
        sys.exit()
else:
    print("The speices you gave is not in our list of speices please double check you have entered it right.")
    sys.exit()

#getting Cd
load_dur = load_dur.lower()
df = pd.read_excel('Wood_tables.xlsx', sheet_name='CD', engine='openpyxl') 
match = df[df["Load Duration"] == load_dur]
if not match.empty:
    match_np = match.to_numpy() # ChatGpt assisted
    Values[0,1] = match_np[0, 1]
    Values[1,1] = match_np[0, 1]
    Values[2,1] = match_np[0, 1]
    Values[4,1] = match_np[0, 1]
else:
    print("The load duration you gave is not in our list of load durations please double check you have entered it right.")
    sys.exit()

# getting CM
if Mouister == True:
    df = pd.read_excel('Wood_tables.xlsx', sheet_name='CM', engine='openpyxl') 
    match = df[df["Size"] == my_class]
    if not match.empty:
        match_np = match.to_numpy() # ChatGpt assisted
        Values[0,2] = match_np[0, 1]
        Values[1,2] = match_np[0, 2]
        Values[2,2] = match_np[0, 3]
        Values[3,2] = match_np[0, 4]
        Values[4,2] = match_np[0, 5]
        Values[5,2] = match_np[0, 6]
        Values[6,2] = match_np[0, 7]

# getting Ct
if T125 == True and T100 == False:
    print("The Temprature statements don,t make logical sense please review them.")
    sys.exit()

if T125 == True:
    Values[1,3] = 0.9
    Values[5,3] = 0.9
    Values[6,3] = 0.9
    if Mouister == False:
        Values[0,3] = 0.7
        Values[2,3] = 0.7
        Values[3,3] = 0.7
        Values[4,3] = 0.7
    else:
        Values[0,3] = 0.5
        Values[2,3] = 0.5
        Values[3,3] = 0.5
        Values[4,3] = 0.5
elif T100 == True:
    Values[1,3] = 0.9
    Values[5,3] = 0.9
    Values[6,3] = 0.9
    if Mouister == False:
        Values[0,3] = 0.8
        Values[2,3] = 0.8
        Values[3,3] = 0.8
        Values[4,3] = 0.8
    else:
        Values[0,3] = 0.7
        Values[2,3] = 0.7
        Values[3,3] = 0.7
        Values[4,3] = 0.7

# getting CF
CF_math = ""
if my_class == "Big":
    Values[1,5] = 1
    Values[4,5] = 1
    if d_act > 12:
         CF_math += "d>12     " + str(d_act) + ">12"
         Values[0,5] = round((12/d_act)**(1/9), 3 )
         CF_math += "\n((12/d_act)**(1/9)     ((12/" + str(d_act) + ")**(1/9) = " + str(Values[0,5])
    else:
        CF_math += "d<12     " + str(d_act) + "<12"
        Values[0,5] = 1
        
else:
    df = pd.read_excel('Wood_tables.xlsx', sheet_name='CF', engine='openpyxl') 
    match = df[df["Grade"] == grade]
    if not match.empty:
        final_match = match[match['Width'] == d_nom] # ChatGPT assisted
        if not final_match.empty:
            final_match_np = final_match.to_numpy()
            if final_match_np[0,5] == "Go To No3":
                df = pd.read_excel('Wood_tables.xlsx', sheet_name='CF', engine='openpyxl') 
                match = df[df["Grade"] == "No3"]
                if not match.empty:
                    final_match = match[match['Width'] == d_nom] # ChatGPT assisted
                    if not final_match.empty:
                        final_match_np = final_match.to_numpy()
                        Values[1,5] = final_match_np[0,5]
                        Values[4,5] = final_match_np[0,6]
                        if b_nom == 2:
                            Values[0,5] = final_match_np[0,2]
                        elif b_nom == 3:
                            Values[0,5] = final_match_np[0,3]
                        elif b_nom == 4:
                            Values[0,5] = final_match_np[0,4]
                        else:
                            print("Something went wrong, the size given was detected to be small but had no CF rule applied so program terminated.")
                            sys.exit()
                    else:
                        print("The specified size is not in the list for CF values.")
                        sys.exit()
                else:
                    print("The specified grade is not in the CF tables and may be due to a mistake in grade for the size of the wood.")
                    sys.exit()
                if final_match_np[0,4] == "NA":
                    print("Utlity cant have 4xless so please rewrite, also if you get this other things have gone wrong since this isn't in size specifications and should have broken sooner.")
                    sys.exit()
            Values[1,5] = final_match_np[0,5]
            Values[4,5] = final_match_np[0,6]
            if b_nom == 2:
                Values[0,5] = final_match_np[0,2]
            elif b_nom == 3:
                Values[0,5] = final_match_np[0,3]
            elif b_nom == 4:
                Values[0,5] = final_match_np[0,4]
            else:
                print("Something went wrong, the size given was detected to be small but had no CF rule applied so program terminated.")
                sys.exit()
        else:
            print("The specified size is not in the list for CF values.")
            sys.exit()
    else:
        print("The specified grade is not in the CF tables and may be due to a mistake in grade for the size of the wood.")
        sys.exit()
if my_class == "Small":
    CM_math =""
    test_1 = Values[0,0]*Values[0,5]
    CM_math += "Fb*CF     " + str(Values[0,0]) + "*" + str(Values[0,5]) + " = " + str(test_1)
    if test_1 <= 1150:
        CM_math += "\nFb*CF ≤ 1150    " + str(test_1) + "≤ 1150 there for CM = 1"
        Values[0,2] = 1
    else:
        CM_math += "\nFb*CF ≥ 1150    " + str(test_1) + "≥ 1150 there for CM = 0.85"
    test_2 = Values[4,0]*Values[4,5]
    CM_math += "\nFc*CF     " + str(Values[4,0]) + "*" + str(Values[0,5]) + " = " + str(test_2)
    if test_2 <= 750:
        CM_math += "\nFc*CF ≤ 750    " + str(test_2) + "≤ 750 there for CM = 1"
        Values[4,2] = 1
    else:
        CM_math += "\nFc*CF ≥ 750    " + str(test_2) + "≥ 750 there for CM = 0.8"

# getting CFu
CFU_values = "CFu " + my_class
if my_class == "Small":
    width = d_nom
    if width >= 10:
        width = "10+"
    df = pd.read_excel('Wood_tables.xlsx', sheet_name=CFU_values, engine='openpyxl') 
    match = df[df["Width"] == width]
    if not match.empty:
        match_np = match.to_numpy()
        if b_nom == 2:
            Values[0,6] = match_np[0,1]
            Values[5,6] = match_np[0,1]
            Values[6,6] = match_np[0,1]
        elif b_nom == 3:
            Values[0,6] = match_np[0,2]
            Values[5,6] = match_np[0,2]
            Values[6,6] = match_np[0,2]
        elif b_nom == 4:
            if final_match_np[0,3] == "NA":
                print("The size is marked as a 4xless so please rewrite, also if you get this other things have gone wrong since this isn't in size specifications and should have broken sooner.")
                sys.exit()
            Values[0,6] = match_np[0,3]
            Values[5,6] = match_np[0,3]
            Values[6,6] = match_np[0,3]
        else:
            print("Something went wrong, the size given was detected to be small but had no CF rule applied so program terminated.")
            sys.exit()
    else:
        print("The width of the provided board is not in the CFu tables. Please double check in put.")
        sys.exit()
else:
    df = pd.read_excel('Wood_tables.xlsx', sheet_name=CFU_values, engine='openpyxl') 
    match = df[df["Grade"] == grade]
    if not match.empty:
        match_np = match.to_numpy()
        Values[0,6] = match_np[0,1]
        Values[5,6] = match_np[0,2]
        Values[6,6] = match_np[0,3]

#getting Ci
if incised == True:
    Values[0,7] = 0.8
    Values[1,7] = 0.8
    Values[2,7] = 0.8
    Values[4,7] = 0.8
    Values[5,7] = 0.95
    Values[6,7] = 0.95
    
# getting Cr
if repetitive == True:
    Values[0,8] = 1.15

#getting CL
CL_math = ""
if d_nom <= b_nom or Lateral == True or braced == True:
    CL_math += "d≤b     " + str(d_nom) + "≤" + str(b_nom) + "    therefore CL = 1"
    Values[0,4] = 1
else:
    CL_math += "d>b     " + str(d_nom) + ">" + str(b_nom)
    Support = Support.lower()
    load = load.lower()
    lu = length*12/d_act
    CL_math += "\nlu/d     " + str(length) + "/" + str(d_act) + " = " + str(lu)
    if Support == "cantilever":
        if load == "uniformly distributed":
            if lu < 7:
                le = 1.33*length
                CL_math += "\nle=1.33lu     1.33*" + str(length) + " = " + str(le)
            else:
                le = 0.9*length+3*d_act
                CL_math += "\nle=0.9lu     0.9*" + str(length) + "+3*" + str(d_act) + " = " + str(le)
        elif  load == "concentrated load at end":
            if lu < 7:
                le = 1.87*length
                CL_math += "\nle=1.87lu     1.87*" + str(length) + " = " + str(le)
            else:
                le = 1.44*length+3*d_act
                CL_math += "\nle=1.44lu     1.44*" + str(length) + "+3*" + str(d_act) + " = " + str(le)
        else:
            print("The load you asgined for the cantilever was not from the two options, double check you chose properly and typed it properly.")
            sys.exit()
    elif Support == "simply supported":
        if load == "uniformly distributed":
            if lu < 7:
                le = 2.06*length
                CL_math += "\nle=2.06lu     2.06*" + str(length) + " = " + str(le)
            else:
                le = 1.63*length+3*d_act
                CL_math += "\nle=1.63lu     1.63*" + str(length) + "+3*" + str(d_act) + " = " + str(le)
        elif load == "concentrated load at center":
            if lu < 7:
                le = 1.8*length
                CL_math += "\nle=1.8lu     1.8*" + str(length) + " = " + str(le)
            else:
                le = 1.37*length+3*d_act
                CL_math += "\nle=1.37lu     1.37*" + str(length) + "+3*" + str(d_act) + " = " + str(le)
        elif load == "2 concentrated loads even with support":
            le = 1.11*length
            CL_math += "\nle=1.11lu     1.11*" + str(length) + " = " + str(le)
        elif load == "3 concentrated loads even with support":
            le = 1.68*length
            CL_math += "\nle=1.68lu     1.68*" + str(length) + " = " + str(le)
        elif load == "4 concentrated loads even with support":
            le = 1.54*length
            CL_math += "\nle=1.54lu     1.54*" + str(length) + " = " + str(le)
        elif load == "5 concentrated loads even with support":
            le = 1.68*length
            CL_math += "\nle=1.68lu     1.68*" + str(length) + " = " + str(le)
        elif load == "6 concentrated loads even with support":
            le = 1.73*length
            CL_math += "\nle=1.73lu     1.73*" + str(length) + " = " + str(le)
        elif load == "7 concentrated loads even with support":
            le = 1.84*length
            CL_math += "\nle=1.84lu     1.84*" + str(length) + " = " + str(le)
        elif load == "equal end moments":
            le = 1.84*length
            CL_math += "\nle=1.84lu     1.84*" + str(length) + " = " + str(le)
        elif load == "Other":
            if lu < 7:
                le = 2.06*length
                CL_math += "\nle=2.06lu     2.06*" + str(length) + " = " + str(le)
            elif lu <= 14.3:
                le = 1.63*length+3*d_act
                CL_math += "\nle=1.63lu+3d     1.63*" + str(length) + "+3*" + str(d_act) + " = " + str(le)
            else:
                le = 1.84*length
                CL_math += "\nle=1.84lu     1.84*" + str(length) + " = " + str(le)
        else:
            print("The load you asgined for the simply supported was not from the ten options, double check you chose properly and typed it properly.")
            sys.exit()
    else:
        print("The support you asgined was not from the two options, double check you chose properly and typed it properly.")
        sys.exit()
    Rb = ((le*d_act)/b_act**2)**(1/2)
    CL_math += "\nRb = √((le*d)/b**2)     √((" + str(le) + "*" + str(d_act) + ")/" + str(b_act) + "^2) = " + str(Rb)
    Emin_prime = math.prod(Values[6])
    CL_math += "\nE_min' = " + str(Values[6,0]) + "*" + str(Values[6,1]) + "*" + str(Values[6,2]) + "*" + str(Values[6,3]) + "*" + str(Values[6,4]) + "*" + str(Values[6,5]) + "*" + str(Values[6,6]) + "*" + str(Values[6,7]) + "*" + str(Values[6,8]) + "*" + str(Values[6,9]) + "*" + str(Values[6,10]) + "*" + str(Values[6,11]) + " = " + str(Emin_prime) + " psi"
    FbE = 1.2*Values[6,0]/Rb**2
    CL_math += "\nFbE = 1.2Emin/Rb^2     1.2*" + str(Values[6,0]) + "/" + str(Rb) + "^2 = " + str(FbE)
    Fbs = math.prod(Values[0])
    CL_math += "\nFb*=" + str(Values[0,0]) + "*" + str(Values[0,1]) + "*" + str(Values[0,2]) + "*" + str(Values[0,3]) + "*" + str(Values[0,5]) + "*" + str(Values[0,6]) + "*" + str(Values[0,7]) + "*" + str(Values[0,8]) + " = " + str(Fbs)
    F = FbE/Fbs
    CL_math += "\nF = FbE/Fb*     " + str(FbE) + "/" + str(Fbs) + " = " + str(F)
    Cl = round((1+F)/1.9-(((1+F)/1.9)**2-F/0.95)**(1/2),3)
    CL_math += "\n(1+F)/1.9-√(((1+F)/1.9)^2-F/0.95)     (1+" + str(F) + ")/1.9-√(((1+" + str(F) + ")/1.9)^2-" + str(F) + "/0.95) = " + str(Cl)
    Values[0,4] = Cl

#getting Cp





#getting CT







#getting Cb




# Getting all adjusted values
new_values = np.zeros(7)
name_table = np.array(["Fb", "Ft", "Fv", "Fc⊥", "Fc", "E", "Emin"])
adjust_table = np.array(["CD", "CM", "Ct", "CL", "CF", "Cfu", "Ci", "Cr", "CP", "CT", "Cb"])
for i in range(7):
    new_values[i] = round(math.prod(Values[i]),3)
mega_table = np.zeros((8,14), dtype=object) # ChatGPT help
mega_table[0,0:2] = " "
mega_table[0,13] = " "
mega_table[1:8,0] = name_table
mega_table[0,2:13] = adjust_table
mega_table[1:8,1:13] = Values
mega_table[1:8,13] = new_values
    
# print out
print("Finding Adjusted values:")
print()
print("Given info:")
print("Size: " + size + "       Grade: " + grade)
print("Speices: " + speices)
print("Load Duration: " + load_dur)
print("Mouister: " + str(Mouister))
if T125 == True:
    print("Temprature: T≥125")
elif T100 == True:
    print("Temprature: 100≤T<125")
else:
    print("Temprature: T<100")
print("Incised: " + str(incised))
print("Repetitive member: " + str(repetitive))
print("length between support: " + str(length) + " ft")
print("Support: " + Support)
print("Load: " + load)
print("Beam length: " + str(length_total) + " ft")
print("Max Moment: " + str(M_max) + " pft")
print("Max Shear: " + str(V_max) + " #")
print("Allowable Deflection: " + str(Δ_allow) + " in")
print("Max Deflection: " + str(Δ_EI) + "/EI in")
print("I_xx: " + str(Ixx) + " in^4")
print("S_xx: " + str(Sxx) + " in^3")
print("A_xx: " + str(A) + " in^2")

#ChatGPT help
fig, ax = plt.subplots(figsize=(12, 4))
ax.axis('off')  # Hide axes

# Create table inside the plot
table = ax.table(
    cellText=mega_table,
    loc='center',
    cellLoc='center'
)

# Optional: scale table
table.auto_set_font_size(True)
#table.set_fontsize(10)
table.scale(1.4, 1.3)

plt.title("Table of Values")
plt.show()
# end of ChatGPT help

print("Math done:")
print("CM math: \n" + CL_math)
print("CF math: \n" + CF_math)
print("Cl math: \n" + CL_math)
for r in range(7):
    print(name_table[r] + " = " + str(Values[r,0]) + "*" + str(Values[r,1]) + "*" + str(Values[r,2]) + "*" + str(Values[r,3]) + "*" + str(Values[r,4]) + "*" + str(Values[r,5]) + "*" + str(Values[r,6]) + "*" + str(Values[r,7]) + "*" + str(Values[r,8]) + "*" + str(Values[r,9]) + "*" + str(Values[r,10]) + "*" + str(Values[r,11]) +" = " + str(new_values[r]) + " psi")

# checks
fb = round(M_max*12/Sxx,3)
print("fb = M*12/S_xx     " + str(M_max) + "*12/" + str(Sxx) + " = " + str(fb) + " psi")
if fb > new_values[0]:
    print("f_b <= F_b'   X rather  f_b > F_b'     " + str(fb) + " > " + str(new_values[0]))
    print("The member is not adequte to support the moment.")
    sys.exit()
print("f_b <= F_b'      " + str(fb) + " <= " + str(new_values[0]) + "   GOOD")

fv = round(1.5*V_max/A,3)
print("fb = 1.5V/A     1.5" + str(V_max) + "/" + str(A) + " = " + str(fv) + " psi")
if fv > new_values[2]:
    print("f_v <= F_v'   X rather  f_v > F_v'     " + str(fv) + " > " + str(new_values[2]))
    print("The member is not adequte to support the shear.")
    sys.exit()
print("f_v <= F_v'      " + str(fv) + " <= " + str(new_values[0]) + "   GOOD")

Δ_max = round(Δ_EI/(Ixx*new_values[5]),3)
print("Δ_max = Δ_EI/E'I_xx     " + str(Δ_EI) + "/(" + str(new_values[5]) + "*" + str(Ixx) + ") = " + str(Δ_max) + " in")
if Δ_max > Δ_allow:
    print("Δ_max <= Δ_allow   X rather  Δ_max > Δ_allow     " + str(Δ_max) + " > " + str(Δ_allow))
    print("The member is not adequte to support the deflection.")
    sys.exit()
print("Δ_max <= Δ_allow     " + str(Δ_max) + " <= " + str(Δ_allow) + "   GOOD")
print("The member is adequate.")
