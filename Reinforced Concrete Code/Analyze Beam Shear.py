# -*- coding: utf-8 -*-
"""
Created on Sat Apr  4 10:58:52 2026

@author: victo
"""

# imports
import numpy as np
import sympy as sp
from scipy.linalg import eigh
import matplotlib.pyplot as plt
import math
import pandas as pd
import sys
from PyQt5.QtWidgets import (QApplication, QDialog, QVBoxLayout, QLabel, QLineEdit, QPushButton, QHBoxLayout, QMessageBox, QComboBox)

class MultiDropDialog(QDialog):
    def __init__(self, questions, options_list):
        super().__init__()
        self.setWindowTitle("Multiple Questions")
        self.setGeometry(1, 30, 1060, 960)

        self.answers = []  # store only selected values

        layout = QVBoxLayout()
        self.combos = []

        for question, options in zip(questions, options_list):
            label = QLabel(question)
            layout.addWidget(label)

            combo = QComboBox()
            combo.addItems(options)
            layout.addWidget(combo)

            self.combos.append(combo)

        button_layout = QHBoxLayout()

        ok_button = QPushButton("OK")
        ok_button.clicked.connect(self.confirm_choices)
        button_layout.addWidget(ok_button)

        cancel_button = QPushButton("Cancel")
        cancel_button.clicked.connect(self.cancel_input)
        button_layout.addWidget(cancel_button)

        layout.addLayout(button_layout)
        self.setLayout(layout)

    def confirm_choices(self):
        self.answers = [combo.currentText() for combo in self.combos]
        self.accept()

    def cancel_input(self):
        self.answers = None
        self.reject()

def MultiDrop(questions, options_list):
    dialog = MultiDropDialog(questions, options_list)
    dialog.exec_()
    if dialog.answers is None:
        sys.exit()
    return dialog.answers

class ChoiceDialog(QDialog):
    def __init__(self, question, options):
        super().__init__()
        self.setWindowTitle(question)
        self.setGeometry(1, 30, 1060, 960)
        self.selected_option = None  # This will store the selected value

        layout = QVBoxLayout()

        for option in options:
            button = QPushButton(option)
            button.clicked.connect(lambda checked, opt=option: self.select_option(opt))
            layout.addWidget(button)

        self.setLayout(layout)
        
        # Add a cancel button
        cancel_button = QPushButton("Cancel")
        cancel_button.clicked.connect(self.cancel_input)
        layout.addWidget(cancel_button)

    def select_option(self, choice):
        self.selected_option = choice
        self.accept()  # Close the dialog and set result to Accepted
    
    def cancel_input(self):
        self.selected_option = None
        self.reject()  # Close the dialog and mark it as rejected

def choice(question, options):
    dialog = ChoiceDialog(question, options)
    dialog.exec_()  # This blocks until the dialog is closed
    if dialog.selected_option is None:
        sys.exit()
    else:
        return dialog.selected_option

class MultiInputDialog(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Test")
        self.setGeometry(1, 30, 1060, 960)
        
        layout = QVBoxLayout()
        self.inputs = []
        
        for question in Questions:
            layout.addWidget(QLabel(question))
            line_edit = QLineEdit()
            layout.addWidget(line_edit)
            self.inputs.append(line_edit)  # Keep reference to get text later

        # Buttons layout
        button_layout = QHBoxLayout()
        submit_btn = QPushButton("Submit")
        cancel_btn = QPushButton("Cancel")
        submit_btn.clicked.connect(self.submit)
        cancel_btn.clicked.connect(self.cancel)

        button_layout.addWidget(submit_btn)
        button_layout.addWidget(cancel_btn)

        layout.addLayout(button_layout)
        self.setLayout(layout)
        self.results = []

    def submit(self):
        """Convert text inputs to floats ('doubles') and handle invalid input."""
        try:
            self.results = [float(inp.text()) for inp in self.inputs]
            self.accept()  # Close dialog if conversion successful
        except ValueError:
            QMessageBox.warning(self, "Invalid Input", "Please enter valid numeric values (e.g. 3.14, -2.5).")

    def cancel(self):
        self.reject()  # Closes dialog and marks it as canceled


def get_inputs():
    dialog = MultiInputDialog()
    if dialog.exec_() == QDialog.Accepted:
        return dialog.results  # Return all answers as a list
    else:
        sys.exit()

Questions = ["f'c (psi)", "b (in)", "h (in)", "d", "cover (in)", "Rebar size for flexure", "Number of flexural bars", "fyt (ksi)", "Rebar Size for shear", "Number of Bands", "Stirrup Legs", "Length total in feet", "Nu on the beam (Kips)", "Weight of concrete (pcf)"]
if __name__ == '__main__':
    fpc, b, h, d, cover, flex_Rebar_Size, bar_number, fyt, Shear_Rebar_Size, Bands, Stirrup_legs, Lt, Nu, wc = get_inputs()
spacing = np.zeros(int(Bands))
Vu = np.zeros(int(Bands))
L_Band = np.zeros(int(Bands))
for i in range(int(Bands)):
    if i == 0:
        Questions = ["Spacing of first band in inches, band at the support, if NONE type 0", "Vu in band being considered in kips",  "Length of band in inches"]
        if __name__ == '__main__':
            spacing[i], Vu[i], L_Band[i] = get_inputs()
    else:
        Questions = ["Spacing of band in inches, if NONE type 0", "Vu in band being considered in kips",  "Length of band in inches"]
        if __name__ == '__main__':
            spacing[i], Vu[i], L_Band[i] = get_inputs()
#checking
if Lt*12/2 > sum(L_Band) or Lt*12/2 < sum(L_Band):
    print("The length of the spacing and the beam are not the same recheck the values you entered.")
    sys.exit()
# finding area of rebar
df = pd.read_excel('Reinforced_Concrete_Tables.xlsx', sheet_name='Rebar_Size', engine='openpyxl') 
match = df[df["Bar number"] == flex_Rebar_Size]
if not match.empty:
    flex_Rebar_Diameter = match.iloc[0, 1]  
    flex_Rebar_Area = match.iloc[0, 2]
else:
    print("The rebar size you typed is not in our list of rebar sizes.")
    sys.exit()
df = pd.read_excel('Reinforced_Concrete_Tables.xlsx', sheet_name='Rebar_Size', engine='openpyxl') 
match = df[df["Bar number"] == Shear_Rebar_Size]
if not match.empty:
    Shear_Rebar_Diameter = match.iloc[0, 1]  
    Shear_Rebar_Area = match.iloc[0, 2]
else:
    print("The rebar size you typed is not in our list of rebar sizes.")
    sys.exit()
As = flex_Rebar_Area*bar_number
print("As = " + str(flex_Rebar_Area) + "*" + str(bar_number) + " = " + str(As) + " in^2")
Av = Shear_Rebar_Area*Stirrup_legs
print("Av = " + str(Shear_Rebar_Area) + "*" + str(Stirrup_legs) + " = " + str(Av) + " in^2")
# getting lamda based on w
if wc <= 100:
    print("wc ≤ 100     " + str(wc) + " ≤ 100 Therefore λ = 0.75")
    lam = 0.75
elif wc >= 135:
    print("wc ≥ 135     " + str(wc) + " ≤ 135 Therefore λ = 1")
    lam = 1
else:
    lam = 0.0075*wc
    print("100 < wc < 135     100 < " + str(wc) + " < 135 Therefore λ = 0.0075*wc     0.0075*" + str(wc) + " = " + str(lam))
smax1 = Av*fyt*1000/(0.75*fpc**0.5*b)
print("Av*fyt*1000/(0.75*√(f'c)*b)     " + str(Av) + "*" + str(fyt) + "*1000/(0.75*√(" + str(fpc) + ")*" + str(b) + ") = " + str(round(smax1,3)) + " in")
smax2 = Av*fyt*1000/(50*b)
print("Av*fyt*1000/(50*b)     " + str(Av) + "*" + str(fyt) + "*1000/(50*" + str(b) + ") = " + str(round(smax2,3)) + " in")
smax = min(smax1, smax2)
print("Use " + str(round(smax,3)) + " in for the max spacing.")
#Vc calc
Vc = np.zeros(int(Bands))
for i in range(int(Bands)):
    if spacing[i] <= smax and spacing[i] != 0:
        print("s ≤ smax     " + str(spacing[i]) + " ≤ " + str(round(smax)) + " Therefor using Eq a.")
        Vc[i] = (2*lam*fpc**0.5+Nu*1000/(6*b*h))*b*d/1000
        print("Vc = [2*λ*√(f'c)+Nu*1000/(6*Ag)]*b*d/1000     [2*" + str(lam) + "*√(" + str(fpc) + ")+" + str(Nu) + "*1000/(6*" + str(b) + "*" + str(h) + ")]*" + str(b) + "*" + str(d) + "/1000 = " + str(round(Vc[i],3)) + " kips")
    else:
        print("s > smax or None which means Eq c.")
        lam_s = (2/(1+d/10))
        print("λs = (2/(1+d/10))     (2/(1+" + str(d) + "/10)) = " + str(round(lam_s,3)))
        if lam_s > 1:
            print("λs > 1 therefore use 1")
            lam_s = 1
        row_w = As/(b*d)
        print("ρw = As/(b*d)     " + str(As) + "/(" + str(b) + "*" + str(d) + ") = " + str(round(row_w,3)))
        Vc[i] = (8*lam_s*lam*row_w**(1/3)*fpc**0.5+Nu*1000/(6*b*h))*b*d/1000
        print("Vc = [8*λs*λ*ρw^(1/3)*√(f'c)+Nu*1000/(6*Ag)]*b*d/1000     [8*" + str(round(lam_s,3)) + "*" + str(lam) + "*" + str(round(row_w,3)) + "^(1/3)*√(" + str(fpc) + ")+" + str(Nu) + "*1000/(6*" + str(b) + "*" + str(h) + ")]*" + str(b) + "*" + str(d) + "/1000 = " + str(round(Vc[i],3)) + " kips")
#Vc max calc
Vc_max = 5*lam*fpc**0.5*b*d/1000
print("Vc_max = 5*λ*√(f'c)*b*d/1000     5*" + str(lam) + "*√(" + str(fpc) + ")*" + str(b) + "*" + str(d) + "/1000 = " + str(round(Vc_max,3)) + " kips")
for i in range(int(Bands)):
    if Vc[i] > Vc_max:
        print("Vc > Vc_max     " + str(round(Vc[i],3)) + " > " + str(round(Vc_max,3)) + " Therefore Vc = " + str(round(Vc_max,3)) + " kips")
        Vc[i] = Vc_max
    else:
        print("Vc ≤ Vc_max     " + str(round(Vc[i],3)) + " ≤ " + str(round(Vc_max,3)) + " Good")
#Cross section dimension check
phiv = 0.75
print("φv = 0.75")
V = 8*fpc**0.5*b*d/1000
print("V = 8*√(f'c)*b*d/1000     8*√(" + str(fpc) + ")*" + str(b) + "*" + str(d) + "/1000 = " + str(round(V,3)) + " kips")
for i in range(int(Bands)):
    if Vu[i] > phiv*(Vc[i]+V):
        print("Vu > φv*(Vc[i]+V)     " + str(Vu[i]) + " > " + str(phiv) + "*(" +str(round(Vc[i],3)) + "+" + str(round(V,3)) + ") = " + str(round(phiv*(Vc[i]+V),3)) + " Therefore cross section dimensions not adequete.")
        sys.exit()
    else:
        print("Vu ≤ φv*(Vc[i]+V)     " + str(round(Vu[i],3)) + " ≤ " + str(phiv) + "*(" +str(round(Vc[i],3)) + "+" + str(round(V,3)) + ") = " + str(round(phiv*(Vc[i]+V),3)) + " Good.")
#Vs calcs
Vs = np.zeros(int(Bands))
for i in range(int(Bands)):
    if spacing[i] == 0:
        Vs[i] = 0
        print("Vs = 0 since no stirrups")
    else:
        Vs[i] = Av*fyt*d/spacing[i]
        print("Vs = Av*fyt*d/s     " + str(Av) + "*" + str(fyt) + "*" + str(d) + "/" + str(spacing[i]) + " = " + str(round(Vs[i],3)) + " kips")
#spacing checks
V_av_check = phiv*lam*fpc**0.5*b*d/1000
print("V_av_check = φv*λ*√(f'c)*b*d/1000     " + str(phiv) + str(lam) + "*√(" + str(fpc) + ")*" + str(b) + "*" + str(d) + "/1000 = " + str(round(V_av_check,3)) + " kips")
V_space_req = 4*fpc**0.5*b*d/1000
print("V = 4*√(f'c)*b*d/1000     4*√(" + str(fpc) + ")*" + str(b) + "*" + str(d) + "/1000 = " + str(round(V_space_req,3)) + " kips")
for i in range(int(Bands)):
    if Vu[i] > V_av_check:
        print("Vu > V_av_check     " + str(round(Vu[i],3)) + " > " + str(round(V_av_check,3)) + " Therefore Av min required")
        if Vs[i] > V_space_req:
            print("Vs > V_space_req     " + str(round(Vs[i],3)) + " > " + str(round(V_space_req,3)))
            smax1 = d/4
            print("smax1 = d/4    " + str(d) + "/4 = " + str(smax1))
            smax2 = 12
            print("smax2 = 12")
            print("smax_current = " + str(round(smax,3)))
            smax_temp = min(smax1,smax2,smax)
            print("smax = " + str(round(smax_temp,3)) + " in")
            if spacing[i] > smax_temp:
                print("s > smax     " + str(spacing[i]) + " > " + str(round(smax_temp,3)) + " Therefore the spacing isn't adequete and the beam fails.")
                sys.exit()
            else:
                print("s ≤ smax     " + str(spacing[i]) + " ≤ " + str(round(smax_temp,3)) + " Good")
            s1_width = d/2
            print("s1_width = d/2    " + str(d) + "/2 = " + str(s1_width))
            s2_width = 12
            print("s2_width = 12")
            s_width = min(s1_width,s2_width)
            print("s_width = " + str(s_width) + " in")
            width = b-2*cover-2*0.5*Shear_Rebar_Diameter
            print("width = b-2*cover-2*0.5*ds     " + str(b) + "-2*" + str(cover) + "-2*0.5*" + str(Shear_Rebar_Diameter) + " = " + str(round(width,3)) + " in")
            if width > s_width:
                print("width > s_width     " + str(width) + " > " + str(s_width) + " Therefore the spacing isn't adequete and the beam fails.")
                sys.exit()
            else:
                print("width ≤ s_width     " + str(width) + " ≤ " + str(s_width) + " Good")
        else:
            print("Vs ≤ V_space_req     " + str(round(Vs[i],3)) + " ≤ " + str(round(V_space_req,3)))
            smax1 = d/2
            print("smax1 = d/2    " + str(d) + "/2 = " + str(smax1))
            smax2 = 24
            print("smax2 = 24")
            print("smax_current = " + str(smax))
            smax_temp = min(smax1,smax2,smax)
            print("smax = " + str(round(smax_temp,3)) + " in")
            if spacing[i] > smax_temp:
                print("s > smax     " + str(spacing[i]) + " > " + str(round(smax_temp,3)) + " Therefore the spacing isn't adequete and the beam fails.")
                sys.exit()
            else:
                print("s ≤ smax     " + str(spacing[i]) + " ≤ " + str(round(smax_temp,3)) + " Good")
            s1_width = d
            print("s1_width = d    " + str(d) + " = " + str(s1_width))
            s2_width = 24
            print("s2_width = 24")
            s_width = min(s1_width,s2_width)
            print("s_width = " + str(s_width) + " in")
            width = b-2*cover-2*0.5*Shear_Rebar_Diameter
            print("width = b-2*cover-2*0.5*ds     " + str(b) + "-2*" + str(cover) + "-2*0.5*" + str(Shear_Rebar_Diameter) + " = " + str(round(width,3)) + " in")
            if width > s_width:
                print("width > s_width     " + str(width) + " > " + str(s_width) + " Therefore the spacing isn't adequete and the beam fails.")
                sys.exit()
            else:
                print("width ≤ s_width     " + str(width) + " ≤ " + str(s_width) + " Good")
    else:
        print("Vu ≤ V_av_check     " + str(round(Vu[i],3)) + " ≤ " + str(round(V_av_check,3)) + " Therefore Av min isn't required and no spacing checks")
#calcing phiv_Vn
phiv_Vn = np.zeros(int(Bands))
for i in range(int(Bands)):
    phiv_Vn[i] = phiv*(Vc[i]+Vs[i])
    print("φvVn = φv*(Vc+Vs)     " + str(phiv) + "*(" + str(round(Vc[i],3)) + "+" + str(round(Vs[i],3)) + ") = " + str(round(phiv_Vn[i],3)) + " kips")
print("The code isn't set to handle checking if adequete for shear since the shear diagrom can look a thousand ways, so ssorry that you need to check by hand.")