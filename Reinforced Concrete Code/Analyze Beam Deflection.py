# -*- coding: utf-8 -*-
"""
Created on Sat Apr  4 11:01:48 2026

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
    app = QApplication.instance() or QApplication(sys.argv)
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
    app = QApplication.instance() or QApplication(sys.argv)
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
    app = QApplication.instance() or QApplication(sys.argv)
    dialog = MultiInputDialog()
    if dialog.exec_() == QDialog.Accepted:
        return dialog.results  # Return all answers as a list
    else:
        sys.exit()

Beam_type = ["Simply Supported", "Cantilever"]
Beam_loading = ["point load", "distributed load"]
Beam_Rebar = ["Singly Reinforced", "Doubly Reinforced"]
T_F = ["True", "False"]
if __name__ == '__main__':
    questions = ["Beam type", "Beam loading","Reinforcement Style", "Supports Non structural Elemnts that mat be damaged"]
    answers = [Beam_type, Beam_loading, Beam_Rebar, T_F]
    B_type, load, rebar_shape, Non_Struct = MultiDrop(questions, answers)

if load == "point load":
    Questions = ["What is the dead load (k)", "What is the live load (k)", "Live Load percent sustained (%)", "Time dependent Factor"]
    if __name__ == '__main__':
        P_d, P_l, percent, zata_s = get_inputs()
elif load == "distributed load":
    Questions = ["What is the dead distributed load (k/ft)", "What is the live distributed load (k/ft)",  "Live Load percent sustained (%)", "Time dependent Factor"]
    if __name__ == '__main__':
        w_d, w_l, percent, zata_s = get_inputs()

if rebar_shape == "Singly Reinforced":
    Questions = ["f'c (psi)", "b (in)", "h (in)", "d (in)", "Rebar size", "Number of bars", "fy (ksi)", "Length (ft)", "weight of concrete (pcf)"]
    if __name__ == '__main__':
        fpc, b, h, d, Low_Rebar_Size, Low_Number_Bars, fy, L, wc = get_inputs()
elif rebar_shape == "Doubly Reinforced":
    Questions = ["f'c (psi)", "b (in)", "h (in)", "Upper d (in)", "Upper Rebar size", "Upper Number of bars", "Low d (in)", "Low Rebar size", "Low Number of bars", "fy (ksi)", "Length (ft)", "weight of concrete (pcf)"]
    if __name__ == '__main__':
        fpc, b, h, d1, Up_Rebar_Size, Up_Number_Bars, d2, Low_Rebar_Size, Low_Number_Bars, fy, L, wc = get_inputs()
#Is deflection check required
if B_type == "Simply Supported":
    h_min = L*12/16
    print("h_min = L*12/16     " + str(L) + "*12/16 = " + str(h_min) + " in")
elif B_type == "Cantilever":
    h_min = L*12/8
    print("h_min = L*12/8     " + str(L) + "*12/8 = " + str(h_min) + " in")
if h_min <= h and Non_Struct == "False":
    print("h_min ≤ h     " + str(h_min) + " ≤ " + str(h) + " and No structural Elements are attached meaning no need to check deflection.")
    sys.exit()
#Finding rebar Area
if rebar_shape == "Singly Reinforced":
    df = pd.read_excel('Reinforced_Concrete_Tables.xlsx', sheet_name='Rebar_Size', engine='openpyxl') 
    match = df[df["Bar number"] == Low_Rebar_Size]
    if not match.empty:
        Low_Rebar_Diameter = match.iloc[0, 1]  
        Low_Rebar_Area = match.iloc[0, 2]
    else:
        print("The rebar size you typed is not in our list of rebar sizes.")
        sys.exit()
    As = Low_Rebar_Area*Low_Number_Bars
    print("As = " + str(Low_Rebar_Area) +"*" + str(Low_Number_Bars))
    Asp = 0
    print("As' = 0")
elif rebar_shape == "Doubly Reinforced":
    df = pd.read_excel('Reinforced_Concrete_Tables.xlsx', sheet_name='Rebar_Size', engine='openpyxl') 
    match = df[df["Bar number"] == Low_Rebar_Size]
    if not match.empty:
        Low_Rebar_Diameter = match.iloc[0, 1]  
        Low_Rebar_Area = match.iloc[0, 2]
    else:
        print("The rebar size you typed is not in our list of rebar sizes.")
        sys.exit()
    df = pd.read_excel('Reinforced_Concrete_Tables.xlsx', sheet_name='Rebar_Size', engine='openpyxl') 
    match = df[df["Bar number"] == Up_Rebar_Size]
    if not match.empty:
        Up_Rebar_Diameter = match.iloc[0, 1]  
        Up_Rebar_Area = match.iloc[0, 2]
    else:
        print("The rebar size you typed is not in our list of rebar sizes.")
        sys.exit()
    As = Low_Rebar_Area*Low_Number_Bars
    print("As = " + str(Low_Rebar_Area) +"*" + str(Low_Number_Bars))
    Asp = Low_Rebar_Area*Low_Number_Bars
    print("As' = " + str(Up_Rebar_Area) +"*" + str(Up_Number_Bars))
# moments of inertia calcs
Ig = 1/12*b*h**3
print("Ig = 1/12*b*h^3     1/12*" + str(b) + "*" + str(h) + "^3 = " + str(Ig) + " in^4")
Ec = wc**1.5*33*fpc**0.5/1000
print("Ec = w^1.5*33*√(f'c)/1000     " + str(wc) + "^1.5*33*√(" + str(fpc) + ")/1000 = " + str(round(Ec,3)) + " ksi")
n = 29000/Ec
print("n = Es/Ec     29000/" + str(round(Ec,3)) + " = " + str(round(n,3)))
if rebar_shape == "Singly Reinforced":
    quad_a = b/2
    print("a = b/2     " + str(b) + "/2 = " + str(quad_a))
    quad_b = n*As
    print(" b = n*As     " + str(round(n,3)) + "*" + str(As) + " = " + str(round(quad_b)))
    quad_c = -n*As*d
    print(" c = -n*As*d     -" + str(round(n,3)) + "*" + str(As) + "*" + str(d) + " = " + str(round(quad_c)))
    c1 = (-quad_b+(quad_b**2-4*quad_a*quad_c)**0.5)/(2*quad_a)
    c2 = (-quad_b-(quad_b**2-4*quad_a*quad_c)**0.5)/(2*quad_a)
    print("c = (-b±√(b^2-4ac)/(2a)     (-" + str(round(quad_b,3)) + "±√(" + str(round(quad_b,3)) + "^2-4*" + str(round(quad_a,3)) + "*" + str(round(quad_c,3)) + ")/(2*" + str(round(quad_a,3)) + ") = " + str(round(c1,3)) + ", " + str(round(c2,3)))
    if c1 < 0 and c2 < 0:
        print("An error occured and both values of c where negative which cant happen, sorry for the inconvienence.")
        sys.exit()
    elif c1 < 0:
        c = c2
        print("Use c = " + str(round(c2,3)) + " in")
    elif c2 < 0:
        c = c1
        print("Use c = " + str(round(c1,3)) + " in")
    elif c1 < c2:
        c = c1
        print("Use c = " + str(round(c1,3)) + " in")
    elif c2 < c1:
        c = c2
        print("Use c = " + str(round(c2,3)) + " in")
    else:
        print("Something went wrong when calculating c sorry for the inconvienence.")
        sys.exit()
    Icr = 1/3*b*c**3+n*As*(c-d)**2
    print("Icr = 1/3*b*c^3+n*As*(c-d)^2     1/3*" + str(b) + "*" + str(round(c)) + "^3+" + str(round(n)) + "*" + str(As) + "*(" + str(round(c)) + "-" + str(d) + "^2 = " + str(round(Icr,3)) + " in^4")
elif rebar_shape == "Doubly Reinforced":
    quad_a = b/2
    print("a = b/2     " + str(b) + "/2 = " + str(quad_a))
    quad_b = n*As+(n-1)*Asp
    print(" b = n*As+(n-1)*Asp     " + str(round(n,3)) + "*" + str(As) + "+(" + str(round(n,3)) + "-1)*" + str(Asp) + " = " + str(round(quad_b)))
    quad_c = -n*As*d-(n-1)*Asp*d
    print(" c = -n*As*d-(n-1)*Asp*d     -" + str(round(n,3)) + "*" + str(As) + "*" + str(d) + "-(" + str(round(n,3)) + "-1)*" + str(Asp) + "*" + str(d) + " = " + str(round(quad_c)))
    c1 = (-quad_b+(quad_b**2-4*quad_a*quad_c)**0.5)/(2*quad_a)
    c2 = (-quad_b-(quad_b**2-4*quad_a*quad_c)**0.5)/(2*quad_a)
    print("c = (-b±√(b^2-4ac)/(2a)     (-" + str(round(quad_b,3)) + "±√(" + str(round(quad_b,3)) + "^2-4*" + str(round(quad_a,3)) + "*" + str(round(quad_c,3)) + ")/(2*" + str(round(quad_a,3)) + ") = " + str(round(c1,3)) + ", " + str(round(c2,3)))
    if c1 < 0 and c2 < 0:
        print("An error occured and both values of c where negative which cant happen, sorry for the inconvienence.")
        sys.exit()
    elif c1 < 0:
        c = c2
        print("Use c = " + str(round(c2,3)) + " in")
    elif c2 < 0:
        c = c1
        print("Use c = " + str(round(c1,3)) + " in")
    elif c1 < c2:
        c = c1
        print("Use c = " + str(round(c1,3)) + " in")
    elif c2 < c1:
        c = c2
        print("Use c = " + str(round(c2,3)) + " in")
    else:
        print("Something went wrong when calculating c sorry for the inconvienence.")
        sys.exit()
    Icr = 1/3*b*c**3+n*As*(c-d)**2
    print("Icr = 1/3*b*c^3+n*As*(c-d)^2     1/3*" + str(b) + "*" + str(round(c)) + "^3+" + str(round(n)) + "*" + str(As) + "*(" + str(round(c)) + "-" + str(d) + "^2 = " + str(round(Icr,3)) + " in^4")
#Mcr Calc
if wc <= 100:
    print("wc ≤ 100     " + str(wc) + " ≤ 100 Therefore λ = 0.75")
    lam = 0.75
elif wc >= 135:
    print("wc ≥ 135     " + str(wc) + " ≤ 135 Therefore λ = 1")
    lam = 1
else:
    lam = 0.0075*wc
    print("100 < wc < 135     100 < " + str(wc) + " < 135 Therefore λ = 0.0075*wc     0.0075*" + str(wc) + " = " + str(lam))
fr = 7.5*lam*fpc**0.5
print("7.5*λ*√(f'c)     7.5*" + str(lam) + "*√(" + str(fpc) + " = " + str(round(fr,3)) + " psi")
yt = h/2
print("yt = h/2     " + str(h) + "/2 = " + str(yt) + " in")
Mcr = fr*Ig/yt/(1000*12)
print("Mcr = fr*Ig/yt/(1000*12)     " + str(fr) + "*" + str(round(Ig,3)) + "/" + str(yt) + "/(1000*12) = " + str(round(Mcr,3)) + " kft")
# moment calcs
if B_type == "Simply Supported":
    if load == "point load":
        print("M = P*L/4")
        M_dl = P_d*L/4
        print("M_dl = " + str(P_d) + "*" + str(L) + "/4 = " + str(M_dl) + " kft")
        M_dl_ll = (P_d+P_l)*L/4
        print("M_dl_ll = (" + str(P_d) + "+" + str(P_l) + ")*" + str(L) + "/4 = " + str(M_dl) + " kft")
    elif load == "distributed load":
        print("M = w*L^2/8")
        M_dl = w_d*L**2/8
        print("M_dl = " + str(w_d) + "*" + str(L) + "^2/8 = " + str(M_dl) + " kft")
        M_dl_ll = (w_d+w_l)*L**2/8
        print("M_dl_ll = (" + str(w_d) + "+" + str(w_l) + ")*" + str(L) + "^2/8 = " + str(M_dl) + " kft")
elif B_type == "Cantilever":
    if load == "point load":
        print("M = P*L")
        M_dl = P_d*L
        print("M_dl = " + str(P_d) + "*" + str(L) + " = " + str(M_dl) + " kft")
        M_dl_ll = (P_d+P_l)*L
        print("M_dl_ll = (" + str(P_d) + "+" + str(P_l) + ")*" + str(L) + " = " + str(M_dl) + " kft")
    elif load == "distributed load":
        print("M = w*L^2/2")
        M_dl = w_d*L**2/2
        print("M_dl = " + str(w_d) + "*" + str(L) + "^2/2 = " + str(M_dl) + " kft")
        M_dl_ll = (w_d+w_l)*L**2/2
        print("M_dl_ll = (" + str(w_d) + "+" + str(w_l) + ")*" + str(L) + "^2/2 = " + str(M_dl) + " kft")
#calcing Ie
if M_dl <= 2/3*Mcr:
    print("M_dl <= 2/3*Mcr     " + str(M_dl) + " ≤ 2/3*" + str(round(Mcr,3)) + " = " + str(round(2/3*Mcr)))
    Ie_dl = Ig
    print("Therefore Ie_dl = Ig     Ie_dl = " + str(round(Ig,3)) + " in^4")
else:
    print("M_dl > 2/3*Mcr     " + str(M_dl) + " > 2/3*" + str(round(Mcr,3)) + " = " + str(round(2/3*Mcr)) + " Need to calc Ie_dl")
    Ie_dl = Icr/(1-(2/3*Mcr/M_dl)**2*(1-Icr/Ig))
    print("Ie_dl = Icr/(1-(2/3*Mcr/M_dl)^2*(1-Icr/Ig))     " + str(round(Icr,3)) + "/(1-(2/3*" + str(round(Mcr,3)) + "/" + str(round(M_dl,3)) + ")^2*(1-" + str(round(Icr,3)) + "/" + str(round(Ig,3)) + " = " + str(Ie_dl) + " in^4")
if M_dl_ll <= 2/3*Mcr:
    print("M_dl_ll ≤ 2/3*Mcr     " + str(M_dl_ll) + " ≤ 2/3*" + str(round(Mcr,3)) + " = " + str(round(2/3*Mcr)))
    Ie_dl_ll = Ig
    print("Therefore Ie_dl_ll = Ig     Ie_dl_ll = " + str(round(Ig,3)) + " in^4")
else:
    print("M_dl_ll > 2/3*Mcr     " + str(M_dl_ll) + " > 2/3*" + str(round(Mcr,3)) + " = " + str(round(2/3*Mcr)) + " Need to calc Ie_dl")
    Ie_dl_ll = Icr/(1-(2/3*Mcr/M_dl_ll)**2*(1-Icr/Ig))
    print("Ie_dl = Icr/(1-(2/3*Mcr/M_dl_ll)^2*(1-Icr/Ig))     " + str(round(Icr,3)) + "/(1-(2/3*" + str(round(Mcr,3)) + "/" + str(round(M_dl_ll,3)) + ")^2*(1-" + str(round(Icr,3)) + "/" + str(round(Ig,3)) + " = " + str(Ie_dl_ll) + " in^4")
# calcing deflections
if B_type == "Simply Supported":
    if load == "point load":
        print("Δ = P*(L*12)^3/(48*Ec*Ie_dl)")
        del_iD = P_d*(L*12)**3/(48*Ec*Ie_dl)
        print("Δ_iD = " + str(P_d) + "*(" + str(L) + "*12)^3/(48*" + str(round(Ec,3)) + "*" + str(round(Ie_dl,3)) + " = " + str(round(del_iD,3)) + " in")
        del_iD_L = (P_d+P_l)*(L*12)**3/(48*Ec*Ie_dl_ll)
        print("Δ_iD_L = (" + str(P_d) + "+" + str(P_l) + ")*(" + str(L) + "*12)^3/(48*" + str(round(Ec,3)) + "*" + str(round(Ie_dl_ll,3)) + " = " + str(round(del_iD_L,3)) + " in")
    elif load == "distributed load":
        print("Δ = 5*w*L^4*12^3/(384*Ec*Ie_dl)")
        del_iD = 5*w_d*L**4*12**3/(384*Ec*Ie_dl)
        print("Δ_iD = 5*" + str(w_d) + "*" + str(L) + "^4*12^3/(384*" + str(round(Ec,3)) + "*" + str(round(Ie_dl,3)) + " = " + str(round(del_iD,3)) + " in")
        del_iD_L = 5*(w_d+w_l)*L**4*12**3/(384*Ec*Ie_dl_ll)
        print("Δ_iD_L = 5*(" + str(w_d) + "+" + str(w_l) + ")*" + str(L) + "^4*12^3/(384*" + str(round(Ec,3)) + "*" + str(round(Ie_dl_ll,3)) + " = " + str(round(del_iD_L,3)) + " in")
elif B_type == "Cantilever":
    if load == "point load":
       print("Δ = P*(L*12)^3/(3*Ec*Ie_dl)")
       del_iD = P_d*(L*12)**3/(3*Ec*Ie_dl)
       print("Δ_iD = " + str(P_d) + "*(" + str(L) + "*12)^3/(3*" + str(round(Ec,3)) + "*" + str(round(Ie_dl,3)) + " = " + str(round(del_iD,3)) + " in")
       del_iD_L = (P_d+P_l)*(L*12)**3/(3*Ec*Ie_dl_ll)
       print("Δ_iD_L = (" + str(P_d) + "+" + str(P_l) + ")*(" + str(L) + "*12)^3/(3*" + str(round(Ec,3)) + "*" + str(round(Ie_dl_ll,3)) + " = " + str(round(del_iD_L,3)) + " in")
    elif load == "distributed load":
        print("Δ = w*L^4*12^3/(8*Ec*Ie_dl)")
        del_iD = w_d*L**4*12**3/(8*Ec*Ie_dl)
        print("Δ_iD = " + str(w_d) + "*" + str(L) + "^4*12^3/(8*" + str(round(Ec,3)) + "*" + str(round(Ie_dl,3)) + " = " + str(round(del_iD,3)) + " in")
        del_iD_L = (w_d+w_l)*L**4*12**3/(8*Ec*Ie_dl_ll)
        print("Δ_iD_L = (" + str(w_d) + "+" + str(w_l) + ")*" + str(L) + "^4*12^3/(8*" + str(round(Ec,3)) + "*" + str(round(Ie_dl_ll,3)) + " = " + str(round(del_iD_L,3)) + " in")
del_iL = del_iD_L-del_iD
print("Δ_iL = Δ_iD_L-Δ_iD     " + str(round(del_iD_L,3)) + "-" + str(round(del_iD,3)) + " = " + str(round(del_iL,3)))
#allowable deflection

# might need to create a question for if floor or flat roof since diffrent
del_short_allowed = L*12/360
print("Δ_short_allowed = L*12/360     " + str(L) + "*12/360 = " + str(round(del_short_allowed)) + " in")
if del_iL > del_short_allowed:
    print("Δ_iL > Δ_short_allowed     " + str(round(del_iL,3)) + " > " + str(round(del_short_allowed,3)) + " Therefore it isn't to code and doesn't work")
    sys.exit()
else:
    print("Δ_iL ≤ Δ_short_allowed     " + str(round(del_iL,3)) + " ≤ " + str(round(del_short_allowed,3)) + " Good")
del_iLs = percent/100*del_iL
print("Δ_iLs = " + str(percent) + "/100*" + str(del_iL) + " = " + str(round(del_iLs,3)) + " in")
lam_infinite = 2/(1+50*Asp/(b*d))
print("λ_∞ = 2/(1+50*As'/(b*d))     2/(1+50*" + str(Asp) + "/(" + str(b) + "*" + str(d) + ")) = " + str(round(lam_infinite)))
lam_t_0 = zata_s/(1+50*Asp/(b*d))
print("λ_t_0 = ζ/(1+50*As'/(b*d))     " + str(zata_s) + "/(1+50*" + str(Asp) + "/(" + str(b) + "*" + str(d) + ")) = " + str(round(lam_t_0)))
lam_t_0_infinite = lam_infinite-lam_t_0
print("λ_t_0_∞ = λ_∞-λ_t_0     " + str(lam_infinite) + "-" + str(lam_t_0) + " = " + str(lam_t_0_infinite))
del_long = lam_t_0_infinite*del_iD+del_iL+lam_infinite*del_iLs
print("Δ_long = λ_t_0_∞*Δ_iD+Δ_iL+λ_∞*Δ_iLs     " + str(lam_t_0_infinite) + "*" + str(round(del_iD,3)) + "+" + str(round(del_iL,3)) + "+" + str(lam_infinite) + "*" + str(round(del_iLs,3)) + " = " + str(round(del_long,3)) + " in")
del_long_allowed = L*12/480
print("Δ_long_allowed = L*12/480     " + str(L) + "*12/480 = " + str(round(del_long_allowed,3)) + " in")
if del_long > del_long_allowed:
    print("Δ_long > Δ_long_allowed     " + str(round(del_long,3)) + " > " + str(round(del_long_allowed,3)) + " Therefore it isn't to code and doesn't work")
    sys.exit()
else:
    print("Δ_long ≤ Δ_long_allowed     " + str(round(del_long,3)) + " ≤ " + str(round(del_long_allowed,3)) + " Good the beam works")
