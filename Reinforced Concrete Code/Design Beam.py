# -*- coding: utf-8 -*-
"""
Created on Sat Apr  4 11:04:22 2026

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
        
question = "What type of beam"
options = ["Singely Reinforced Known Dimensions","Singely Reinforced Unknown Dimensions"]
if __name__ == "__main__":
    beam_type = choice(question, options)
# Asking for all required values
Beam_type = ["Simply Supported", "Cantilever"]
Beam_loading = ["point load", "distributed load"]
T_F = ["True", "False"]
Weather = ["No exposure to weather or ground", "Exposed to weather or ground", "Cast against and constant contact with ground"]
if __name__ == '__main__':
    questions = ["Beam type", "Beam loading", "Supports Non structural Elemnts that mat be damaged", "What type of exposure", "Can Shear be taken d away from support"]
    answers = [Beam_type, Beam_loading, T_F, Weather, T_F]
    B_type, load, Non_Struct, exposure, d_away = MultiDrop(questions, answers)

if load == "point load":
    Questions = ["What is the dead load (k)", "What is the live load (k)", "Live Load percent sustained (%)", "Time dependent Factor"]
    if __name__ == '__main__':
        P_d, P_l, percent, zata_s = get_inputs()
elif load == "distributed load":
    Questions = ["What is the dead distributed load (k/ft)", "What is the live distributed load (k/ft)",  "Live Load percent sustained (%)", "Time dependent Factor"]
    if __name__ == '__main__':
        w_d, w_l, percent, zata_s = get_inputs()

if beam_type == "Singely Reinforced Known Dimensions":
    Questions = ["f'c (psi)", "b (in)", "h (in)", "fy (ksi)", "Nu (k)", "Length of beam (ft)", "Aggergate size", "Weight of Concrete pcf", "fyt (ksi)", "Stirrup Leg Size", "Number of legs"]
    if __name__ == '__main__':
        fpc, b, h, fy, Nu, L, dagg, wc, fyt, Stirrup_size, Legs = get_inputs()
    # finding values of Vu,Mu, and partial deflection
    if B_type == "Simply Supported":
        if load == "point load":
            # load combos
            P1 = 1.6*P_d
            print("P1 = 1.6D     1.6*" + str(P_d) + " = " + str(P1) + " kips")
            P2 = 1.2*P_d+1.4*P_l
            print("P1 = 1.2D+1.4L     1.2*" + str(P_d) + "1.4*" + str(P_l) + " = " + str(P2) + " kips")
            P = max(P1,P2)
            print("Therefor use P = " + str(P) + " kips")
            # solving
            Vu = P/2
            print("Vu = P/2     " + str(P) + "/2 = " + str(Vu) + " kips")
            Mu = P*L/4
            print("Mu = PL/4     " + str(P) + "*" + str(L) + "/4 = " + str(Mu) + " kip ft")
            print("Δ*EI = P*(L*12)^3/(48)")
            del_iD_EI = P_d*(L*12)**3/(48)
            print("Δ_iD*EI = " + str(P_d) + "*(" + str(L) + "*12)^3/(48) = " + str(round(del_iD_EI,3)))
            del_iD_L_EI = (P_d+P_l)*(L*12)**3/(48)
            print("Δ_iD_L*EI = (" + str(P_d) + "+" + str(P_l) + ")*(" + str(L) + "*12)^3/(48) = " + str(round(del_iD_L_EI,3)))
        elif load == "distributed load":
            # load combos
            W1 = 1.6*w_d
            print("W1 = 1.6D     1.6*" + str(w_d) + " = " + str(W1) + " kips")
            W2 = 1.2*w_d+1.4*w_l
            print("W1 = 1.2D+1.4L     1.2*" + str(w_d) + "1.4*" + str(w_l) + " = " + str(W2) + " kips")
            W = max(W1,W2)
            print("Therefor use W = " + str(W) + " kips")
            # solving
            Vu = W*L/2
            print("Vu = WL/2     " + str(W) + "*" + str(L) + "/2 = " + str(Vu) + " kip")
            Mu = W*L**2/8
            print("Mu = WL^2/8     " + str(W) + "*" + str(L) + "^2/8 = " + str(Mu) + " kip ft")
            print("Δ*EI = 5*w*L^4*12^3/(384)")
            del_iD_EI = 5*w_d*L**4*12**3/(384)
            print("Δ_iD*EI = 5*" + str(w_d) + "*" + str(L) + "^4*12^3/(384) = " + str(round(del_iD_EI,3)))
            del_iD_L_EI = 5*(w_d+w_l)*L**4*12**3/(384)
            print("Δ_iD_L*EI = 5*(" + str(w_d) + "+" + str(w_l) + ")*" + str(L) + "^4*12^3/(384) = " + str(round(del_iD_L_EI,3)))
    elif B_type == "Cantilever":
        if load == "point load":
            # load combos
            P1 = 1.6*P_d
            print("P1 = 1.6D     1.6*" + str(P_d) + " = " + str(P1) + " kips")
            P2 = 1.2*P_d+1.4*P_l
            print("P1 = 1.2D+1.4L     1.2*" + str(P_d) + "1.4*" + str(P_l) + " = " + str(P2) + " kips")
            P = max(P1,P2)
            print("Therefor use P = " + str(P) + " kips")
            # solving
            Vu = P
            print("Vu = P = " + str(P) + " kips")
            Mu = P*L
            print("Mu = PL     " + str(P) + "*" + str(L) + " = " + str(Mu) + " kip ft")
            print("Δ*EI = P*(L*12)^3/(3)")
            del_iD_EI = P_d*(L*12)**3/(3)
            print("Δ_iD*EI = " + str(P_d) + "*(" + str(L) + "*12)^3/(3) = " + str(round(del_iD_EI,3)) + " in")
            del_iD_L_EI = (P_d+P_l)*(L*12)**3/(3)
            print("Δ_iD_L*EI = (" + str(P_d) + "+" + str(P_l) + ")*(" + str(L) + "*12)^3/(3) = " + str(round(del_iD_L_EI,3)) + " in")
        elif load == "distributed load":
            W1 = 1.6*w_d
            print("W1 = 1.6D     1.6*" + str(w_d) + " = " + str(W1) + " kips")
            W2 = 1.2*w_d+1.4*w_l
            print("W1 = 1.2D+1.4L     1.2*" + str(w_d) + "1.4*" + str(w_l) + " = " + str(W2) + " kips")
            W = max(W1,W2)
            print("Therefor use W = " + str(W) + " kips")
            # solving
            Vu = W*L
            print("Vu = WL     " + str(W) + "*" + str(L) + " = " + str(Vu) + " kip")
            Mu = W*L**2/2
            print("Mu = WL^2/2     " + str(W) + "*" + str(L) + "^2/2 = " + str(Mu) + " kip ft")
            print("Δ*EI = w*L^4*12^3/(8)")
            del_iD_EI = w_d*L**4*12**3/(8)
            print("Δ_iD*EI = " + str(w_d) + "*" + str(L) + "^4*12^3/(8) = " + str(round(del_iD_EI,3)) + " in")
            del_iD_L_EI = (w_d+w_l)*L**4*12**3/(8)
            print("Δ_iD_L*EI = (" + str(w_d) + "+" + str(w_l) + ")*" + str(L) + "^4*12^3/(8) = " + str(round(del_iD_L_EI,3)) + " in")
    # find required area of steel
    phif = 0.9
    print("φf = 0.9")
    if b <= h:
        j = 0.9
        print("j = 0.9")
    else:
        j = 0.95
        print("j = 0.95")
    if exposure == "No exposure to weather or ground":
        cover = 1.5
        print("Cover = 1.5 in")
    elif exposure == "Exposed to weather or ground":
        cover = 2
        print("Cover = 2 in")
    elif exposure == "Cast against and constant contact with ground":
        cover = 3
        print("Cover = 3 in")
    d = h-cover-1
    print("d = h-cover-1     " + str(h) + "-" + str(cover) + "-1 = " + str(d) + " in")
    As_req = Mu*12/(phif*fy*j*d)
    print("As_req = Mu*12/(φf*fy*j*d)     " + str(Mu) + "*12/" + str(phif) + "*" + str(fy) + "*" + str(j) + "*" + str(d) + " = " + str(round(As_req,3)) + " in^2")
    df = pd.read_excel('Reinforced_Concrete_Tables.xlsx', sheet_name='Rebar_Size', engine='openpyxl') 
    match = df[df["Bar number"] == Stirrup_size]
    if not match.empty:
        shear_rebar_diameter = match.iloc[0, 1]  
        shear_rebar_area = match.iloc[0, 2]  
    else:
        print("The rebar size you typed is not in our list of rebar sizes.")
        sys.exit()
    flexure_rebar = [6, 7, 8, 9]
    flexure_rebar_diameter = np.zeros(len(flexure_rebar))
    flexure_rebar_area = np.zeros(len(flexure_rebar))
    num_of_bars = np.zeros(len(flexure_rebar))
    As = np.zeros(len(flexure_rebar))
    rows = ["1","1","1","1"]
    flexure_rebar_math = ["", "", "", ""]
    s = np.zeros(len(flexure_rebar))
    d = np.zeros(len(flexure_rebar))
    d1 = np.zeros(len(flexure_rebar))
    d2 = np.zeros(len(flexure_rebar))
    c = np.zeros(len(flexure_rebar))
    PhifMn = np.zeros(len(flexure_rebar))
    dc_ratio = np.zeros(len(flexure_rebar))
    for i in range(len(flexure_rebar)):
        # finding area of rebar
        df = pd.read_excel('Reinforced_Concrete_Tables.xlsx', sheet_name='Rebar_Size', engine='openpyxl') 
        match = df[df["Bar number"] == flexure_rebar[i]]
        if not match.empty:
            flexure_rebar_diameter[i] = match.iloc[0, 1]  
            flexure_rebar_area[i] = match.iloc[0, 2]  
        else:
            print("The rebar size you typed is not in our list of rebar sizes.")
            sys.exit()
        flexure_rebar_math[i] += "Rebar size: " + str(flexure_rebar[i])
        flexure_rebar_math[i] += "\n"
        num_of_bars[i] = As_req/flexure_rebar_area[i]
        flexure_rebar_math[i] += "\n#_bars = " + str(round(As_req,3)) + "/" + str(flexure_rebar_area[i]) + " = " + str(round(num_of_bars[i],3))
        num_of_bars[i] = round(num_of_bars[i]+0.5)
        if num_of_bars[i] == 1:
            num_of_bars[i] =2
        flexure_rebar_math[i] += "\nTherefore #_bars is = " + str(num_of_bars[i])
        As[i] = flexure_rebar_area[i]*num_of_bars[i]
        flexure_rebar_math[i] += "\nAs = " + str(flexure_rebar_area[i]) + "*" + str(num_of_bars[i]) + " = " + str(As[i]) + " in^2"
        smin1 = 1
        flexure_rebar_math[i] += "\nsmin1 = " + str(smin1) + " in"
        smin2 = flexure_rebar_diameter[i]
        flexure_rebar_math[i] += "\nsmin2 = d_b = " + str(smin2) + " in"
        smin3 = 4/3*dagg
        flexure_rebar_math[i] += "\nsmin2 = 4/3*dagg = 4/3" + str(dagg) + " = " + str(smin3) + " in"
        smin = max(smin1,smin2,smin3)
        flexure_rebar_math[i] += "\nTherefore smin = " + str(smin) + " in"
        stirrup_bend = 2*shear_rebar_diameter-flexure_rebar_diameter[i]/2
        flexure_rebar_math[i] += "\nstirrup_bend = 2*" + str(shear_rebar_diameter) + "-" + str(flexure_rebar_diameter[i]) + "/2 = " + str(round(stirrup_bend,3)) + " in"
        b_min = 2*cover+Legs*shear_rebar_diameter+Legs*stirrup_bend+num_of_bars[i]*flexure_rebar_diameter[i]+(num_of_bars[i]-1)*smin
        flexure_rebar_math[i] += "\nb_min = 2*" + str(cover) + "+" + str(Legs) + "*" + str(shear_rebar_diameter) + "+" + str(Legs) + "*" + str(round(stirrup_bend,3)) + "+" + str(num_of_bars[i]) + "*" + str(flexure_rebar_diameter[i]) + "+(" + str(num_of_bars[i]) + "-1)*" + str(smin) + " = " + str(round(b_min,3)) + " in"
        if b_min > b:
            flexure_rebar_math[i] += "\nb_min > b     " + str(round(b_min,3)) + " > " + str(b) + " Therefore need more than 1 row."
            b_min = 4*cover+Legs*2*shear_rebar_diameter+Legs*2*stirrup_bend+num_of_bars[i]*flexure_rebar_diameter[i]+(num_of_bars[i]-1)*smin
            flexure_rebar_math[i] += "\nb_min = 4*" + str(cover) + "+" + str(Legs) + "*2*" + str(shear_rebar_diameter) + "+" + str(Legs) + "*2*" + str(round(stirrup_bend,3)) + "+" + str(num_of_bars[i]) + "*" + str(flexure_rebar_diameter[i]) + "+(" + str(num_of_bars[i]) + "-1)*" + str(smin) + " = " + str(round(b_min,3)) + " in"
            rows[i] = "2"
        if b_min > 2*b:
            flexure_rebar_math[i] += "\nb_min > 2*b     " + str(round(b_min,3)) + " > " + str(2*b) + " Therefore need more than 2 rows and code not set up for that."
            rows[i] = "2+"
        if rows[i] == "2+":
            flexure_rebar_math[i] += "\n rows: " + rows[i] + " Therefore code cant continue from here."
        else:
            flexure_rebar_math[i] += "\n rows: " + rows[i]
            smax1 = 15*40/(2/3*fy)-2.5*(cover+shear_rebar_diameter)
            flexure_rebar_math[i] += "\nsmax1 = 15*40/(2/3*fy)-2.5(cover+d_s)     15*40/(2/3*" + str(fy) + ")-2.5(" + str(cover) + "+" + str(shear_rebar_diameter) + ") = " + str(round(smax1,3)) + " in"
            smax2 = 12*40/(2/3*fy)
            flexure_rebar_math[i] += "\nsmax2 = 12*40/(2/3*fy)     12*40/(2/3*" + str(fy) + ") = " + str(round(smax2,3)) + " in"
            smax = min(smax1,smax2)
            flexure_rebar_math[i] += "\nTherfore smax = " + str(round(smax,3)) + " in"
            # Bar spacing could be upgraded probably should be but for know it is this
            
            
            if rows[i] == "2":
                s[i] = smin+(b-b_min/2)/(round(num_of_bars[i]/2+0.5)-1)
                flexure_rebar_math[i] += "\ns = smin+(b-b_min)/(num_of_bars-1)     " + str(round(smin,3)) + "+(" + str(b) + "-" + str(round(b_min/2,3)) + ")/(" + str(round(num_of_bars[i]/2+0.5)) + "-1) = " + str(round(s[i],3)) + " in"
                num_of_bars[i] = round(num_of_bars[i]+0.5)
                flexure_rebar_math[i] += "\nChanging number of bars to work for code, previous bar count might work better though. = " + str(num_of_bars[i])
                As[i] = flexure_rebar_area[i]*num_of_bars[i]
                flexure_rebar_math[i] += "\nAs = " + str(flexure_rebar_area[i]) + "*" + str(num_of_bars[i]) + " = " + str(round(As[i],3)) + " in^2"
                d1[i] = h-cover-shear_rebar_diameter-0.5*flexure_rebar_diameter[i]
                flexure_rebar_math[i] += "\nd1 = h-cover-d_s-0.5*d_b     " + str(h) + "-" + str(cover) + "-" + str(shear_rebar_diameter) + "-0.5*" + str(flexure_rebar_diameter) + " = " + str(round(d1[i],3)) + " in"
                d1[i] = round(d1[i]-0.5)+0.5
                flexure_rebar_math[i] += "\nTherfore d1 = " + str(d1[i]) + " in"
                sminv = 1
                flexure_rebar_math[i] += "\nsminv = " + str(sminv) + " in"
                d2[i] = d1[i]-flexure_rebar_diameter[i]-sminv
                flexure_rebar_math[i] += "\nd2 = d1-d_b-sminv" + str(round(d1[i],3)) + "-" + str(flexure_rebar_diameter[i]) + "-" + str(sminv) + " = " + str(round(d2[i],3)) + " in"
                d2[i] = round(d2[i]-0.5)+0.5
                flexure_rebar_math[i] += "\nTherfore d2 = " + str(d2[i]) + " in"
                d[i] = As[i]/2*(d1[i]+d2[i])/As[i]
                flexure_rebar_math[i] += "\nd = As*(d1+d2)/As_t     " + str(As[i]/2) + "*(" + str(d1[i]) + "+" + str(d2[i]) + ")/" + str(As[i]) + " = " + str(d[i]) + " in"
            elif rows[i] == "1":
                s[i] = smin+(b-b_min)/(num_of_bars[i]-1)
                flexure_rebar_math[i] += "\ns = smin+(b-b_min)/(num_of_bars-1)     " + str(round(smin,3)) + "+(" + str(b) + "-" + str(round(b_min,3)) + ")/(" + str(num_of_bars[i]) + "-1) = " + str(round(s[i],3)) + " in"
                d[i] = h-cover-shear_rebar_diameter-0.5*flexure_rebar_diameter[i]
                flexure_rebar_math[i] += "\nd = h-cover-d_s-0.5*d_b     " + str(h) + "-" + str(cover) + "-" + str(shear_rebar_diameter) + "-0.5*" + str(flexure_rebar_diameter[i]) + " = " + str(round(d[i],3)) + " in"
                d[i] = round(d[i]-0.5)+0.5 #rounding down to nearest half theoreticly
                d1[i] = d[i]
                d2[i] = d[i]
                flexure_rebar_math[i] += "\nTherfore d = " + str(d[i]) + " in"
            flexure_rebar_math[i] += "\nChecking if it works."
            #Finding c and a
            if fpc <= 4000:
                flexure_rebar_math[i] += "\nf'c ≤ 4000 so β1 = 0.85"
                beta1 = 0.85
            elif fpc >= 8000:
                flexure_rebar_math[i] += "\nf'c ≥ 8000 so β1 = 0.65"
                beta1 = 0.65
            else:
                flexure_rebar_math[i] += "\n4000 ≤ f'c ≤ 8000"
                beta1 = 0.85 - (0.05*(fpc-4000)/1000)
                flexure_rebar_math[i] += "\nβ1 = 0.85-0.05(f'c-4000)/1000     0.85-0.05(" + str(fpc) + "-4000)/1000 = " + str(round(beta1,3))
            c[i] = As[i]*fy*1000/(0.85*fpc*beta1*b)
            flexure_rebar_math[i] += "\nc = As*fy*1000/(0.85*f'c*β1*b)     " + str(As[i]) + "*" + str(fy) + "*1000/(0.85*" + str(fpc) + "*" + str(round(beta1,3)) + "*" + str(b) + ") = " + str(round(c[i],3)) + " in"
            a = beta1*c[i]
            flexure_rebar_math[i] += "\na = β1*c     " + str(round(beta1,3)) + "*" + str(round(c[i],3)) + " = " + str(round(a,3)) + " in"
            # checking strain
            if rows[i] == "2":
                ecu = 0.003
                flexure_rebar_math[i] += "\nεcu = 0.003"
                es = ecu*(d2[i]-c[i])/c[i]
                flexure_rebar_math[i] += "\nεs = εcu(d2-c)/c     " + str(ecu) + "(" + str(d2[i]) + "-" + str(round(c[i],3)) + ")/" + str(round(c[i],3)) + " = " + str(round(es,5))
                ey = fy/29000
                flexure_rebar_math[i] += "\nεy = fy/29000     " + str(fy) + "/29000 = " + str(round(ey,5))
                if es >= ey:
                    flexure_rebar_math[i] += "\nεs = " + str(round(es,5)) + " ≥ εy = " + str(round(ey,5)) + " GOOD"
                    est = ecu*(d1[i]-c[i])/c[i]
                    flexure_rebar_math[i] += "\nεs = εcu(d1-c)/c     " + str(ecu) + "(" + str(d1[i]) + "-" + str(round(c[i],3)) + ")/" + str(round(c[i],3)) + " = " + str(round(est,5))   
                    if est >= ey + 0.003:
                        flexure_rebar_math[i] += "\nεt = " + str(round(est,5)) + " ≥ εy + 0.003 = " + str(round(ey,5)) + " + 0.003 = " + str(round(ey+0.003,5))+ " GOOD"
                        flexure_rebar_math[i] += "\nTherefore Φf = 0.9"
                        phif = 0.9
                        PhifMn[i] = phif*As[i]*fy*(d[i]-a/2)/12
                        flexure_rebar_math[i] += "\nΦfMn = Φf*As*fy*(d-a/2)/12     " + str(phif) + "*" + str(As[i]) + "*" + str(fy) + "*(" + str(d[i]) + "-" + str(round(a,3)) + "/2)/12 = " + str(round(PhifMn[i],3)) + " kft"
                        if PhifMn[i] < Mu:
                            flexure_rebar_math += "\nΦfMn < Mu     " + str(round(PhifMn[i])) + " < " + str(round(Mu)) + " Beam fails NO GOOD"
                        else:
                            flexure_rebar_math += "\nΦfMn ≥ Mu     " + str(round(PhifMn[i],3)) + " ≥ " + str(round(Mu,3)) + " GOOD"
                            dc_ratio[i] = Mu/PhifMn[i]
                            flexure_rebar_math[i] += "\ndc_ratio = Mu/ΦfMn     " + str(Mu) + "/" + str(round(PhifMn[i],3)) + " = " + str(round(dc_ratio[i],3))
                            # Checking Asmin
                            Asmin1 = 3*(fpc)**(1/2)/(fy*1000)*b*d[i]
                            flexure_rebar_math[i] += "\nAsmin1 = 3√(fpc)/(fy*1000)*b*d     3√(" + str(fpc) + ")/(" + str(fy) + "*1000)*" + str(b) + "*" + str(d[i]) + " = " + str(round(Asmin1,3)) + " in^2"
                            Asmin2 = 200/(fy*1000)*b*d[i]
                            flexure_rebar_math[i] += "\nAsmin2 = 200/(fy*1000)*b*d     200/(" + str(fy) + "*1000)*" + str(b) + "*" + str(d[i]) + " = " + str(round(Asmin2,3)) + " in^2"
                            Asmin = max(Asmin1, Asmin2)
                            flexure_rebar_math[i] += "\nAsmin = " + str(round(Asmin,3)) + " in^2"
                            if As[i] >= Asmin:
                                flexure_rebar_math[i] += "\nAs = " + str(round(As[i],3)) + " ≥ Asmin = " + str(round(Asmin,3)) + " GOOD"
                            else:
                                flexure_rebar_math[i] += "\nAs = " + str(round(As[i],3)) + " ≥ Asmin = " + str(round(Asmin,3)) + " NO Beam fails"
                    else:
                        flexure_rebar_math[i] += "\nεt = " + str(round(es,5)) + " ≥ εy + 0.003 = " + str(round(ey,5)) + " + 0.003 = " + str(round(ey+0.003,5))+ " NO"
                        flexure_rebar_math[i] += "\nFails Φf = 0.9"
                else:
                    flexure_rebar_math[i] += "\εs = " + str(round(es,5)) + " ≥ εy = " + str(round(ey,5)) + " NO, and wont pass Φf = 0.9 since εt ≥ ey + 0.003"
                    #Note possible it might pass if d is big enough but doutful and at that point probably closer to double reinforced.
                    #leaving space and note incase we decide to add it.
            elif rows[i] == "1":
                ecu = 0.003
                flexure_rebar_math[i] += "\nεcu = 0.003"
                es = ecu*(d[i]-c[i])/c[i]
                flexure_rebar_math[i] += "\nεs = εcu(d-c)/c     " + str(ecu) + "(" + str(d[i]) + "-" + str(round(c[i],3)) + ")/" + str(round(c[i],3)) + " = " + str(round(es,5))
                ey = fy/29000
                flexure_rebar_math[i] += "\nεy = fy/29000     " + str(fy) + "/29000 = " + str(round(ey,5))
                if es >= ey:
                    flexure_rebar_math[i] += "\nεs = " + str(round(es,5)) + " ≥ εy = " + str(round(ey,5)) + " GOOD"
                    if es >= ey + 0.003:
                        flexure_rebar_math[i] += "\nεt = " + str(round(es,5)) + " ≥ εy + 0.003 = " + str(round(ey,5)) + " + 0.003 = " + str(round(ey+0.003,5))+ " GOOD"
                        flexure_rebar_math[i] += "\nTherefore Φf = 0.9"
                        phif = 0.9
                        PhifMn[i] = phif*As[i]*fy*(d[i]-a/2)/12
                        flexure_rebar_math[i] += "\nΦfMn = Φf*As*fy*(d-a/2)/12     " + str(phif) + "*" + str(As[i]) + "*" + str(fy) + "*(" + str(d[i]) + "-" + str(round(a,3)) + "/2)/12 = " + str(round(PhifMn[i],3)) + " kft"
                        dc_ratio[i] = Mu/PhifMn[i]
                        flexure_rebar_math[i] += "\ndc_ratio = Mu/ΦfMn     " + str(Mu) + "/" + str(round(PhifMn[i],3)) + " = " + str(round(dc_ratio[i],3))
                        # Checking Asmin
                        Asmin1 = 3*(fpc)**(1/2)/(fy*1000)*b*d[i]
                        flexure_rebar_math[i] += "\nAsmin1 = 3√(fpc)/(fy*1000)*b*d     3√(" + str(fpc) + ")/(" + str(fy) + "*1000)*" + str(b) + "*" + str(d[i]) + " = " + str(round(Asmin1,3)) + " in^2"
                        Asmin2 = 200/(fy*1000)*b*d[i]
                        flexure_rebar_math[i] += "\nAsmin2 = 200/(fy*1000)*b*d     200/(" + str(fy) + "*1000)*" + str(b) + "*" + str(d[i]) + " = " + str(round(Asmin2,3)) + " in^2"
                        Asmin = max(Asmin1, Asmin2)
                        flexure_rebar_math[i] += "\nAsmin = " + str(round(Asmin,3)) + " in^2"
                        if As[i] >= Asmin:
                            flexure_rebar_math[i] += "\nAs = " + str(round(As[i],3)) + " ≥ Asmin = " + str(round(Asmin,3)) + " GOOD"
                        else:
                            flexure_rebar_math[i] += "\nAs = " + str(round(As[i],3)) + " ≥ Asmin = " + str(round(Asmin,3)) + " NO Beam fails"
                    else:
                        flexure_rebar_math[i] += "\nεt = " + str(round(es,5)) + " ≥ εy + 0.003 = " + str(round(ey,5)) + " + 0.003 = " + str(round(ey+0.003,5))+ " NO"
                        flexure_rebar_math[i] += "\nFails Φf = 0.9"
                else:
                    flexure_rebar_math[i] += "\nεs = " + str(round(es,5)) + " ≥ εy = " + str(round(ey,5)) + " NO, and wont pass Φf = 0.9 since εt ≥ ey + 0.003"
    #printing all math for Flexure check
    for i in range(len(flexure_rebar)):
        print(flexure_rebar_math[i])
    #quick flexure overview
    for i in range(len(flexure_rebar)):
        print("dc_ratio of " + str(num_of_bars[i]) + " #" + str(flexure_rebar[i]) + "bars: " + str(round(dc_ratio[i],3)))
    #shear desgin
    # only pulling working values
    counter = 0
    for i in range(len(flexure_rebar)):
        if d[i] != 0:
            counter +=1
    d_shear = np.zeros(counter)
    working_bar = np.zeros(counter)
    working_bar_number = np.zeros(counter)
    placement = 0
    for i in range(len(flexure_rebar)):
        if d[i] != 0:
            d_shear[placement] = d[i]
            working_bar[placement] = flexure_rebar[i] 
            working_bar_number[placement] = num_of_bars[i] 
            placement +=1
    Vu_d = np.zeros(counter)
    shear_math = [""]*counter
    # finding Vu@d
    for i in range(counter):
        if d_away == "True":
            if load == "point load":
                Vu_d[i] = Vu
                shear_math[i] += "\nVu@d is just Vu since no change."
            elif load == "distributed load":
                Vu_d[i] = Vu-W*d_shear[i]/12
                shear_math[i] += "\nVu@d = Vu-W*d/12     " + str(round(Vu,3)) + "-" + str(round(W,3)) + "*" + str(d_shear[i]) + "/12 = " + str(round(Vu_d[i],3))
        else:
            Vu_d[i] = Vu
            shear_math[i] += "\nVu since not taking d away."
    # How many bands/ Band strength
    phiv = 0.75
    print("\nΦv = 0.75")
    if wc <= 100:
        print("wc ≤ 100     " + str(wc) + " ≤ 100 Therefore λ = 0.75")
        lam = 0.75
    elif wc >= 135:
        print("wc ≥ 135     " + str(wc) + " ≤ 135 Therefore λ = 1")
        lam = 1
    else:
        lam = 0.0075*wc
        print("100 < wc < 135     100 < " + str(wc) + " < 135 Therefore λ = 0.0075*wc     0.0075*" + str(wc) + " = " + str(lam))
    No_Stirrup = np.zeros(counter)
    phiv_Vc = np.zeros(counter)
    for i in range(counter):
        No_Stirrup[i] = phiv*lam*fpc**0.5*b*d_shear[i]/1000
        shear_math[i] += "\nNo Stirrup = Φv*λ*√(f'c)*b*d/1000     " + str(phiv) + "*" + str(lam) + "*√(" + str(fpc) + ")*" + str(b) + "*" + str(d_shear[i]) + "/1000 = " + str(round(No_Stirrup[i],3)) + " k"
        phiv_Vc[i] = phiv*(2*lam*fpc**0.5/1000+Nu/(6*b*h))*b*d_shear[i]
        shear_math[i] += "\nΦvVc = Φv(2*λ*√(f'c)/1000+Nu/(6*b*h))*b*d    " + str(phiv) + "(2*" + str(lam) + "*√(" + str(fpc) + ")/1000+" + str(Nu) + "/(6*" + str(b) + "*" + str(h) + "*" + str(b) + "))*" + str(d_shear[i]) + "/1000 = " + str(round(phiv_Vc[i],3)) + " k"
    #creating bands
    V = np.zeros(counter)
    V_analyze = np.zeros(counter)
    smax = np.zeros(counter)
    across_smax = np.zeros(counter)
    if load == "point load":
        bands = 1
        for i in range(counter):
            if Vu_d[i] <= No_Stirrup[i]:
                shear_math[i] += "\nVu@d = " + str(round(Vu_d[i],3)) + " ≤ " + str(round(No_Stirrup[i],3)) + " Therefore no stirrups required along beam since point load."
            elif Vu_d[i] > phiv_Vc[i]:
                shear_math[i] += "\nVu@d = " + str(round(Vu_d[i],3)) + " > " + str(round(phiv_Vc[i],3))
                V[i] = Vu_d[i]/phiv-phiv_Vc[i]/phiv
                shear_math[i] += "\nVu@d/Φv-ΦvVc/Φv     " + str(round(Vu_d[i],3)) + "/" + str(phiv) + "-" + str(round(phiv_Vc[i],3)) + "/" + str(phiv) + str(round(V[i],3))
                V_analyze[i] = 4*fpc**0.5*b*d_shear[i]/1000
                shear_math[i] += "\n4√(f'c)*b*d/1000     4*√(" + str(fpc) + ")*" + str(b) + "*" + str(d_shear[i]) + "/1000 = " + str(round(V_analyze[i],3)) + " k"
                if V[i] <= V_analyze[i]:
                    shear_math[i] += "\n" + str(round(V[i],3)) + " ≤ " + str(round(V_analyze[i],3))
                    smax1 = d_shear[i]/2
                    shear_math[i] += "\nsmax1 = d/2     " + str(d_shear[i]) + "/2 = " + str(smax1) + " in"
                    smax2 = 24
                    shear_math[i] += "\nsmax2 = 24 in"
                    smax1 = min(smax1,smax2)
                    shear_math[i] += "\nsmax = " + str(smax1) + " in"
                    s = b-2*cover-Legs*0.5*shear_rebar_diameter
                    shear_math[i] += "\n Does the number of legs work"
                    shear_math[i] += "\ns = b-2*cover-Legs*0.5*ds     " + str(b) +"-2*" + str(cover) + "-" + str(Legs) + "*0.5*" + str(shear_rebar_diameter) + " = " + str(round(s,3)) + " in" 
                    across_smax1 = d[i]
                    shear_math[i] += "\nacross_smax1 = d     " + str(d[i]) + " = " + str(across_smax1) + " in"
                    across_smax2 = 24
                    shear_math[i] += "\nacross_smax2 = 24 in"
                    across_smax[i] = min(across_smax1,across_smax2)
                    shear_math[i] += "\nacross_smax = " + str(across_smax[i]) + " in"
                    if s > across_smax[i]:
                        shear_math[i] += "\ns > across_smax     " + str(round(s,3)) + " > " + str(across_smax[i])
                        shear_math[i] += "\nThe number of legs isn't adequete you need to increase the leg number by at least 1"
                    else:
                        shear_math[i] += "\ns ≤ across_smax     " + str(round(s,3)) + " ≤ " + str(across_smax[i]) + " GOOD"
                else:
                    shear_math[i] += "\n" + str(round(V[i],3)) + " > " + str(round(V_analyze[i],3))
                    smax1 = d_shear[i]/4
                    shear_math[i] += "\nsmax1 = d/4     " + str(d_shear[i]) + "/4 = " + str(smax1) + " in"
                    smax2 = 12
                    shear_math[i] += "\nsmax2 = 12 in"
                    smax1 = min(smax1,smax2)
                    shear_math[i] += "\nsmax = " + str(smax1) + " in"
                    s = b-2*cover-Legs*0.5*shear_rebar_diameter
                    shear_math[i] += "\n Does the number of legs work"
                    shear_math[i] += "\ns = b-2*cover-Legs*0.5*ds     " + str(b) +"-2*" + str(cover) + "-" + str(Legs) + "*0.5*" + str(shear_rebar_diameter) + " = " + str(round(s,3)) + " in" 
                    across_smax1 = d[i]/2
                    shear_math[i] += "\nacross_smax1 = d/2     " + str(d[i]) + "/2 = " + str(across_smax1) + " in"
                    across_smax2 = 12
                    shear_math[i] += "\nacross_smax2 = 12 in"
                    across_smax[i] = min(across_smax1,across_smax2)
                    shear_math[i] += "\nacross_smax = " + str(across_smax[i]) + " in"
                    if s > across_smax[i]:
                        shear_math[i] += "\ns > across_smax     " + str(round(s,3)) + " > " + str(across_smax[i])
                        shear_math[i] += "\nThe number of legs isn't adequete you need to increase the leg number by at least 1"
                    else:
                        shear_math[i] += "\ns ≤ across_smax     " + str(round(s,3)) + " ≤ " + str(across_smax[i]) + " GOOD"
                Av = shear_rebar_area*Legs
                shear_math[i] += "\nAv = " + str(shear_rebar_area) + "*" + str(Legs) + " = " + str(Av) + " in^2"
                smax2 = Av*fyt*1000/(0.75*fpc**0.5*b)
                shear_math[i] += "\nsmax1 = Av*fyt*1000/(0.75*√(f'c)*b)     " + str(Av) + "*" + str(fyt) + "*1000/(0.75*√(" + str(fpc) + ")*" + str(b) + ") = " + str(round(smax2,3)) + " in"
                smax3 = Av*fyt*1000/(50*b)
                shear_math[i] += "\nsmax2 = Av*fyt*1000/(50*b)     " + str(Av) + "*" + str(fyt) + "*1000/(50*" + str(b) + ") = " + str(round(smax3,3)) + " in"
                smax1 = min(smax1,smax2,smax3)
                shear_math[i] += "\nsmax = " + str(round(smax1,3)) + " in"
                smax2 = phiv*Av*fyt*d_shear[i]/(Vu_d[i]-phiv_Vc[i])
                shear_math[i] += "\nsmax1 = Φv*Av*fyt*d/(Vu@d-ΦvVc)     " + str(phiv) + "*" + str(Av) + "*" + str(fyt) + "*" + str(d_shear[i]) + "/(" + str(round(Vu_d[i],3)) + "-" + str(round(phiv_Vc,3)) + ") = " + str(round(smax2,3))
                smax[i] = min(smax1,smax2)
                shear_math[i] += "\nsmax = " + str(round(smax[i],3)) + " in"
                smax[i] = round(smax[i]-0.5)
                shear_math[i] += "\nTherefore smax = " + str(smax[i]) + " in"
            else:
                shear_math[i] += "\n" + str(round(No_Stirrup[i],3)) + " < Vu@d = " + str(round(Vu_d[i],3)) + " ≤ " + str(round(phiv_Vc[i],3))
                V[i] = Vu_d[i]/phiv-phiv_Vc[i]/phiv
                shear_math[i] += "\nVu@d/Φv-ΦvVc/Φv     " + str(round(Vu_d[i],3)) + "/" + str(phiv) + "-" + str(round(phiv_Vc[i],3)) + "/" + str(phiv) + str(round(V[i],3))
                V_analyze[i] = 4*fpc**0.5*b*d_shear[i]/1000
                shear_math[i] += "\n4√(f'c)*b*d/1000     4*√(" + str(fpc) + ")*" + str(b) + "*" + str(d_shear[i]) + "/1000 = " + str(round(V_analyze[i],3)) + " k"
                if V[i] <= V_analyze[i]:
                    shear_math[i] += "\n" + str(round(V[i],3)) + " ≤ " + str(round(V_analyze[i],3))
                    smax1 = d_shear[i]/2
                    shear_math[i] += "\nsmax1 = d/2     " + str(d_shear[i]) + "/2 = " + str(smax1) + " in"
                    smax2 = 24
                    shear_math[i] += "\nsmax2 = 24 in"
                    smax1 = min(smax1,smax2)
                    shear_math[i] += "\nsmax = " + str(smax1) + " in"
                    s = b-2*cover-Legs*0.5*shear_rebar_diameter
                    shear_math[i] += "\n Does the number of legs work"
                    shear_math[i] += "\ns = b-2*cover-Legs*0.5*ds     " + str(b) +"-2*" + str(cover) + "-" + str(Legs) + "*0.5*" + str(shear_rebar_diameter) + " = " + str(round(s,3)) + " in" 
                    across_smax1 = d[i]
                    shear_math[i] += "\nacross_smax1 = d     " + str(d[i]) + " = " + str(across_smax1) + " in"
                    across_smax2 = 24
                    shear_math[i] += "\nacross_smax2 = 24 in"
                    across_smax[i] = min(across_smax1,across_smax2)
                    shear_math[i] += "\nacross_smax = " + str(across_smax[i]) + " in"
                    if s > across_smax[i]:
                        shear_math[i] += "\ns > across_smax     " + str(round(s,3)) + " > " + str(across_smax[i])
                        shear_math[i] += "\nThe number of legs isn't adequete you need to increase the leg number by at least 1"
                    else:
                        shear_math[i] += "\ns ≤ across_smax     " + str(round(s,3)) + " ≤ " + str(across_smax[i]) + " GOOD"
                else:
                    shear_math[i] += "\n" + str(round(V[i],3)) + " > " + str(round(V_analyze[i],3))
                    smax1 = d_shear[i]/4
                    shear_math[i] += "\nsmax1 = d/4     " + str(d_shear[i]) + "/4 = " + str(smax1) + " in"
                    smax2 = 12
                    shear_math[i] += "\nsmax2 = 12 in"
                    smax1 = min(smax1,smax2)
                    shear_math[i] += "\nsmax = " + str(smax1) + " in"
                    s = b-2*cover-Legs*0.5*shear_rebar_diameter
                    shear_math[i] += "\n Does the number of legs work"
                    shear_math[i] += "\ns = b-2*cover-Legs*0.5*ds     " + str(b) +"-2*" + str(cover) + "-" + str(Legs) + "*0.5*" + str(shear_rebar_diameter) + " = " + str(round(s,3)) + " in" 
                    across_smax1 = d[i]/2
                    shear_math[i] += "\nacross_smax1 = d/2     " + str(d[i]) + "/2 = " + str(across_smax1) + " in"
                    across_smax2 = 12
                    shear_math[i] += "\nacross_smax2 = 12 in"
                    across_smax[i] = min(across_smax1,across_smax2)
                    shear_math[i] += "\nacross_smax = " + str(across_smax[i]) + " in"
                    if s > across_smax[i]:
                        shear_math[i] += "\ns > across_smax     " + str(round(s,3)) + " > " + str(across_smax[i])
                        shear_math[i] += "\nThe number of legs isn't adequete you need to increase the leg number by at least 1"
                    else:
                        shear_math[i] += "\ns ≤ across_smax     " + str(round(s,3)) + " ≤ " + str(across_smax[i]) + " GOOD"
                Av = shear_rebar_area*Legs
                shear_math[i] += "\nAv = " + str(shear_rebar_area) + "*" + str(Legs) + " = " + str(Av) + " in^2"
                smax2 = Av*fyt*1000/(0.75*fpc**0.5*b)
                shear_math[i] += "\nsmax1 = Av*fyt*1000/(0.75*√(f'c)*b)     " + str(Av) + "*" + str(fyt) + "*1000/(0.75*√(" + str(fpc) + ")*" + str(b) + ") = " + str(round(smax2,3)) + " in"
                smax3 = Av*fyt*1000/(50*b)
                shear_math[i] += "\nsmax2 = Av*fyt*1000/(50*b)     " + str(Av) + "*" + str(fyt) + "*1000/(50*" + str(b) + ") = " + str(round(smax3,3)) + " in"
                smax[i] = min(smax1,smax2,smax3)
                shear_math[i] += "\nsmax = " + str(round(smax[i],3)) + " in"
                smax[i] = round(smax[i]-0.5)
                shear_math[i] += "\nTherefore smax = " + str(smax[i]) + " in"
    else:
        # creating V along whole beam
        if B_type == "Simply Supported":
            number_of_x = round(L/2*12+1)
        elif B_type == "Cantilever":
            number_of_x = round(L*12+1)
        x_line = np.zeros(number_of_x)
        V_of_beam = np.zeros(number_of_x)
        for i in range(number_of_x):
            x_line[i] = i/12
            if i == number_of_x-1:
                x_line[i] = L
            if B_type == "Simply Supported":
                V_of_beam[i] += W*(L/2-x_line[i])
            elif B_type == "Cantilever":
                V[i] += -W*x_line[i]
        x_change = np.zeros((len(d_shear),3))
        for r in range(len(d_shear)):
            x_change[r,0] = -phiv_Vc[r]/(W)+L/2
            shear_math[r] += "\nL1 = -ϕvVc/(W)+L/2     -" + str(phiv_Vc) + "/" + str(W) + "+" + str(L) + "/2 = " + str(x_change[r,0]) + " ft"
            x_change[r,1] = -No_Stirrup[r]/(W)+L/2
            shear_math[r] += "\nL1 = -No_stirrup/(W)+L/2     -" + str(No_Stirrup) + "/" + str(W) + "+" + str(L) + "/2 = " + str(x_change[r,1]) + " ft"
        # bands being set up
        band_counter = np.ones(len(d_shear))
        for r in range(len(d_shear)):
            for col in range(3):
                if x_change[r,col] > 0:
                    band_counter[r] +=1     
        bands = int(max(band_counter))
        spacing = np.zeros((len(d_shear),bands))
        for r in range(len(d_shear)):
            cur_band = 0
            Av = shear_rebar_area*Legs
            shear_math[r] += "\nAv = " + str(shear_rebar_area) + "*" + str(Legs) + " = " + str(Av) + " in^2"
            for col in range(3):
                if bands == 3:
                    if x_change[r,col] > 0 and cur_band == 0:
                        smax1 = d_shear[r]/4
                        shear_math[r] += "\nsmax1 = d/4     " + str(d_shear[r]) + "/4 = " + str(smax1) + " in"
                        smax2 = Av*fyt*1000/(0.75*fpc**0.5*b)
                        shear_math[r] += "\nsmax2 = Av*fyt*1000/(0.75*√(f'c)*b)     " + str(Av) + "*" + str(fyt) + "*1000/(0.75*√(" + str(fpc) + ")*" + str(b) + ") = " + str(round(smax2,3)) + " in"
                        smax3 = Av*fyt*1000/(50*b)
                        shear_math[r] += "\nsmax3 = Av*fyt*1000/(50*b)     " + str(Av) + "*" + str(fyt) + "*1000/(50*" + str(b) + ") = " + str(round(smax3,3)) + " in"
                        smax4 = 12
                        shear_math[r] += "\nsmax4 = 12 in"
                        spacing[r,cur_band] = int(min(smax1,smax2,smax3,smax4))
                        cur_band += 1
                    elif x_change[r,col] > 0 and cur_band == 1:
                        smax1 = d_shear[r]/2
                        shear_math[r] += "\nsmax1 = d/2     " + str(d_shear[r]) + "/2 = " + str(smax1) + " in"
                        smax2 = Av*fyt*1000/(0.75*fpc**0.5*b)
                        shear_math[r] += "\nsmax2 = Av*fyt*1000/(0.75*√(f'c)*b)     " + str(Av) + "*" + str(fyt) + "*1000/(0.75*√(" + str(fpc) + ")*" + str(b) + ") = " + str(round(smax2,3)) + " in"
                        smax3 = Av*fyt*1000/(50*b)
                        shear_math[r] += "\nsmax3 = Av*fyt*1000/(50*b)     " + str(Av) + "*" + str(fyt) + "*1000/(50*" + str(b) + ") = " + str(round(smax3,3)) + " in"
                        smax4 = 24
                        shear_math[r] += "\nsmax4 = 24 in"
                        spacing[r,cur_band] = int(min(smax1,smax2,smax3,smax4))
                        cur_band += 1
                elif bands == 2:
                    if x_change[r,col] > 0:
                        smax1 = d_shear[r]/4
                        shear_math[r] += "\nsmax1 = d/4     " + str(d_shear[r]) + "/4 = " + str(smax1) + " in"
                        smax2 = Av*fyt*1000/(0.75*fpc**0.5*b)
                        shear_math[r] += "\nsmax2 = Av*fyt*1000/(0.75*√(f'c)*b)     " + str(Av) + "*" + str(fyt) + "*1000/(0.75*√(" + str(fpc) + ")*" + str(b) + ") = " + str(round(smax2,3)) + " in"
                        smax3 = Av*fyt*1000/(50*b)
                        shear_math[r] += "\nsmax3 = Av*fyt*1000/(50*b)     " + str(Av) + "*" + str(fyt) + "*1000/(50*" + str(b) + ") = " + str(round(smax3,3)) + " in"
                        smax4 = 12
                        shear_math[r] += "\nsmax4 = 12 in"
                        spacing[r,cur_band] = int(min(smax1,smax2,smax3,smax4))
                        shear_math[r] += "\nsmax = " + str(spacing[r,cur_band])
                        cur_band += 1
            # finalizing spaces and lengths
            Ls_S = x_change
            for r in range(len(d_shear)):
                if bands == 3:
                    Ls_S[r,0] = round(x_change[r,0]*12/spacing[r,0]+.5,0)*spacing[r,0]
                    shear_math[r] += "\nLength1 = next_whole_number(l1*12/s1)*s1     next_whole_number(l" + str(x_change[r,0]) + "*12/" + str(spacing[r,0]) + ")*" + str(spacing[r,0]) + " = " + str(Ls_S[r,0]) + " in"
                    Ls_S[r,1] = round(x_change[r,1]*12/spacing[r,1]+.5,0)*spacing[r,1]
                    shear_math[r] += "\nLength1 = next_whole_number(l2*12/s2)*s2     next_whole_number(l" + str(x_change[r,1]) + "*12/" + str(spacing[r,1]) + ")*" + str(spacing[r,1]) + " = " + str(Ls_S[r,1]) + " in"
                elif bands == 2:
                    Ls_S[r,0] = round(x_change[r,0]*12/spacing[r,0]+.5,0)*spacing[r,0]
                    shear_math[r] += "\nLength1 = next_whole_number(l1*12/s1)*s1     next_whole_number(l" + str(x_change[r,0]) + "*12/" + str(spacing[r,0]) + ")*" + str(spacing[r,0]) + " = " + str(Ls_S[r,0]) + " in"
            #printing all math for Shear design
            for i in range(len(d_shear)):
                print(shear_math[i])
            #quick shear overview
            print("Shear Overview for " + str(Stirrup_size) + " with " + str(Legs) + ".")
            for i in range(len(d_shear)):
                if bands == 3:
                    print(str(working_bar[i]) + ": Band1 = Stops at " + str(Ls_S[i,0]) + " in spaced at " + str(spacing[i,0]) + " in.")
                    print("     Band2 = Stops at " + str(Ls_S[i,1]) + " in spaced at " + str(spacing[i,1]) + " in.")
                    if B_type == "Simply Supported":
                        print("     No stirrups required for remaining half of beam and the two halfs are mirrors of eachother.")
                    elif B_type == "Cantilever":
                        print("     No stirrups required for the rest of the beam")
                elif bands == 2:
                    print(working_bar[i] + ": Band1 = Stops at " + str(Ls_S[i,0]) + " in spaced at " + str(spacing[i,0]) + " in.")
                    if B_type == "Simply Supported":
                        print("     No stirrups required for remaining half of beam and the two halfs are mirrors of eachother.")
                    elif B_type == "Cantilever":
                        print("     No stirrups required for the rest of the beam")
                elif load == "point load":
                    print(str(working_bar[i]) + ": Only 1 Band spaced at " + str(smax[i]) + " in.")
    #deflection solving
    # set values since not designing doubly reinforced
    rebar_shape = "Singly Reinforced"
    Asp = 0
    del_long = np.zeros(len(d_shear))
    for i in range(len(d_shear)):
        print("Deflection for beam with " + str(num_of_bars[i]) + " #" + str(flexure_rebar[i]) + "bars: ")
        if B_type == "Simply Supported":
            h_min = L*12/16
            print("h_min = L*12/16     " + str(L) + "*12/16 = " + str(h_min) + " in")
        elif B_type == "Cantilever":
            h_min = L*12/8
            print("h_min = L*12/8     " + str(L) + "*12/8 = " + str(h_min) + " in")
        if h_min <= h and Non_Struct == "False":
            print("h_min ≤ h     " + str(h_min) + " ≤ " + str(h) + " and No structural Elements are attached meaning no need to check deflection.")
            sys.exit()
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
            quad_b = n*As[i]
            print(" b = n*As     " + str(round(n,3)) + "*" + str(As) + " = " + str(round(quad_b)))
            quad_c = -n*As[i]*d_shear[i]
            print(" c = -n*As*d     -" + str(round(n,3)) + "*" + str(As) + "*" + str(d_shear[i]) + " = " + str(round(quad_c)))
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
            Icr = 1/3*b*c**3+n*As[i]*(c-d_shear[i])**2
            print("Icr = 1/3*b*c^3+n*As*(c-d)^2     1/3*" + str(b) + "*" + str(round(c)) + "^3+" + str(round(n)) + "*" + str(As) + "*(" + str(round(c)) + "-" + str(d_shear[i]) + "^2 = " + str(round(Icr,3)) + " in^4")
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
        lam_infinite = 2/(1+50*Asp/(b*d_shear[i]))
        print("λ_∞ = 2/(1+50*As'/(b*d))     2/(1+50*" + str(Asp) + "/(" + str(b) + "*" + str(d_shear[i]) + ")) = " + str(round(lam_infinite)))
        lam_t_0 = zata_s/(1+50*Asp/(b*d_shear[i]))
        print("λ_t_0 = ζ/(1+50*As'/(b*d))     " + str(zata_s) + "/(1+50*" + str(Asp) + "/(" + str(b) + "*" + str(d_shear[i]) + ")) = " + str(round(lam_t_0)))
        lam_t_0_infinite = lam_infinite-lam_t_0
        print("λ_t_0_∞ = λ_∞-λ_t_0     " + str(lam_infinite) + "-" + str(lam_t_0) + " = " + str(lam_t_0_infinite))
        del_long[i] = lam_t_0_infinite*del_iD+del_iL+lam_infinite*del_iLs
        print("Δ_long = λ_t_0_∞*Δ_iD+Δ_iL+λ_∞*Δ_iLs     " + str(lam_t_0_infinite) + "*" + str(round(del_iD,3)) + "+" + str(round(del_iL,3)) + "+" + str(lam_infinite) + "*" + str(round(del_iLs,3)) + " = " + str(round(del_long[i],3)) + " in")
        del_long_allowed = L*12/480
        print("Δ_long_allowed = L*12/480     " + str(L) + "*12/480 = " + str(round(del_long_allowed,3)) + " in")
        if del_long[i] > del_long_allowed:
            print("Δ_long > Δ_long_allowed     " + str(round(del_long[i],3)) + " > " + str(round(del_long_allowed,3)) + " Therefore it isn't to code and doesn't work")
        else:
            print("Δ_long ≤ Δ_long_allowed     " + str(round(del_long[i],3)) + " ≤ " + str(round(del_long_allowed,3)) + " Good the beam works")
    # Deflection over view
    print("Deflection Overview")
    for i in range(len(d_shear)):
        print("A displacement of " + str(round(del_long[i],3)) + " in occured in the beam with " + str(working_bar_number[i]) + " #" + str(working_bar[i]) + "bars" )
    
    #All info printed in one for flexure shear and deflection
    print()
    print()
    print("Overview for Beams Designed")
    for i in range(len(d_shear)):
        print("For the beam with " + str(working_bar_number[i]) + " #" + str(working_bar[i]) + "bars: The D/C ratio:" + str(round(dc_ratio[i],3)))
        if bands == 3:
            print("Band1 = Stops at " + str(Ls_S[i,0]) + " in spaced at " + str(spacing[i,0]) + " in.")
            print("     Band2 = Stops at " + str(Ls_S[i,1]) + " in spaced at " + str(spacing[i,1]) + " in.")
            if B_type == "Simply Supported":
                print("     No stirrups required for remaining half of beam and the two halfs are mirrors of eachother.")
            elif B_type == "Cantilever":
                print("     No stirrups required for the rest of the beam")
        elif bands == 2:
            print("Band1 = Stops at " + str(Ls_S[i,0]) + " in spaced at " + str(spacing[i,0]) + " in.")
            if B_type == "Simply Supported":
                print("     No stirrups required for remaining half of beam and the two halfs are mirrors of eachother.")
            elif B_type == "Cantilever":
                print("     No stirrups required for the rest of the beam")
        elif load == "point load":
            print("Only 1 Band spaced at " + str(smax[i]) + " in.")
        print("A displacement of " + str(round(del_long[i],3)) + " in occured ")
        print()
                
                
                
                
                
                
                
                
                
                
                
                
                
                
                
                
                
                
                