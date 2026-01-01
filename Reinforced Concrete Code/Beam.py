# -*- coding: utf-8 -*-
"""
Created on Fri Oct 24 09:10:59 2025

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

# Desgin or Analysis which are we doing
question = "Are we Desgining or Analyzing"
options = ["Desgining", "Analyzing"]
if __name__ == "__main__":
    procedure = choice(question, options)

# based on answer above. what else do we need and then the math.
if procedure == "Analyzing":
    # Which version of a beam
    question = "What style is the beam"
    options = ["Singely Reinforced One Layer", "Singely Reinforced Two Layer" , "T or L", "Doubbly Reinforced", "Shear", "Deflection"]
    if __name__ == "__main__":
        beam_type = choice(question, options)
    # Asking for all required values and then solving
    if beam_type == "Singely Reinforced One Layer":
        Questions = ["f'c (psi)", "b (in)", "h (in)", "d (in)", "fy (ksi)", "Rebar Size", "Number of Rebar"]
        if __name__ == '__main__':
            fpc, b, h, d, fy, Rebar_Size, Rebar_Count = get_inputs()
            # finding area of rebar
            df = pd.read_excel('Reinforced_Concrete_Tables.xlsx', sheet_name='Rebar_Size', engine='openpyxl') 
            match = df[df["Bar number"] == Rebar_Size]
            if not match.empty:
                Rebar_Diameter = match.iloc[0, 1]  
                Rebar_area = match.iloc[0, 2]  
            else:
                print("The rebar size you typed is not in our list of rebar sizes.")
                sys.exit()
            As = Rebar_Count*Rebar_area
            print("As = " + str(Rebar_Count) + "*" + str(Rebar_area) + " = " + str(As) + " in^2")
            #Finding c and a
            if fpc <= 4000:
                print("f'c ≤ 4000 so β1 = 0.85")
                beta1 = 0.85
            elif fpc >= 8000:
                print("f'c ≥ 8000 so β1 = 0.65")
                beta1 = 0.65
            else:
                print("4000 ≤ f'c ≤ 8000")
                beta1 = 0.85 - (0.05*(fpc-4000)/1000)
                print("β1 = 0.85-0.05(f'c-4000)/1000     0.85-0.05(" + str(fpc) + "-4000)/1000 = " + str(round(beta1,3)))
            c = As*fy*1000/(0.85*fpc*beta1*b)
            print("c = As*fy*1000/(0.85*f'c*β1*b)     " + str(As) + "*" + str(fy) + "*1000/(0.85*" + str(fpc) + "*" + str(round(beta1,3)) + "*" + str(b) + ") = " + str(round(c,3)) + " in")
            a = beta1*c
            print("a = β1*c     " + str(round(beta1,3)) + "*" + str(round(c,3)) + " = " + str(round(a,3)) + " in")
            # checking flexural steel
            ecu = 0.003
            print("εcu = 0.003")
            es = ecu*(d-c)/c
            print("εs = εcu(d-c)/c     " + str(ecu) + "(" + str(d) + "-" + str(round(c,3)) + ")/" + str(round(c,3)) + " = " + str(round(es,5)))
            ey = fy/29000
            print("εy = fy/29000     " + str(fy) + "/29000 = " + str(round(ey,5)))
            if es >= ey:
                print("εs = " + str(round(es,5)) + " ≥ εy = " + str(round(ey,5)) + " GOOD")
            else:
                print("εs = " + str(round(es,5)) + " ≥ εy = " + str(round(ey,5)) + " NO, and wont pass Φf = 0.9 since εt ≥ ey + 0.003")
                sys.exit()
            if es >= ey + 0.003:
                print("εt = " + str(round(es,5)) + " ≥ εy + 0.003 = " + str(round(ey,5)) + " + 0.003 = " + str(round(ey+0.003,5))+ " GOOD")
                print("Therefore Φf = 0.9")
                phif = 0.9
            else:
                print("εt = " + str(round(es,5)) + " ≥ εy + 0.003 = " + str(round(ey,5)) + " + 0.003 = " + str(round(ey+0.003,5))+ " NO")
                print("Fails Φf = 0.9")
                sys.exit()
            # Calculating PhifMn
            PhifMn = phif*As*fy*(d-a/2)/12
            print("ΦfMn = Φf*As*fy*(d-a/2)/12     " + str(phif) + "*" + str(As) + "*" + str(fy) + "*(" + str(d) + "-" + str(round(a,3)) + "/2)/12 = " + str(round(PhifMn,3)) + " kft")
            # Checking Asmin
            Asmin1 = 3*(fpc)**(1/2)/(fy*1000)*b*d
            print("Asmin1 = 3√(fpc)/(fy*1000)*b*d     3√(" + str(fpc) + ")/(" + str(fy) + "*1000)*" + str(b) + "*" + str(d) + " = " + str(round(Asmin1,3)) + " in^2")
            Asmin2 = 200/(fy*1000)*b*d
            print("Asmin2 = 200/(fy*1000)*b*d     200/(" + str(fy) + "*1000)*" + str(b) + "*" + str(d) + " = " + str(round(Asmin2,3)) + " in^2")
            Asmin = max(Asmin1, Asmin2)
            print("Asmin = " + str(round(Asmin,3)) + " in^2")
            if As >= Asmin:
                print("As = " + str(round(As,3)) + " ≥ Asmin = " + str(round(Asmin,3)) + " GOOD")
            else:
                print("As = " + str(round(As,3)) + " ≥ Asmin = " + str(round(Asmin,3)) + " NO Beam fails")
    
    # code to run single reinforcment with multiple layers of same bar type
    if beam_type == "Singely Reinforced Two Layer":
        Questions = ["f'c (psi)", "b (in)", "h (in)", "Top steel d1 (in)", "Low steel d2 (in)", "fy (ksi)", "Rebar Size", "Top Number of Rebar", "Bottom Number of Rebar"]
        if __name__ == '__main__':
            fpc, b, h, d1, d2, fy, Rebar_Size, Top_Rebar_Count, Bottom_Rebar_Count = get_inputs()
            # finding area of rebar
            df = pd.read_excel('Reinforced_Concrete_Tables.xlsx', sheet_name='Rebar_Size', engine='openpyxl') 
            match = df[df["Bar number"] == Rebar_Size]
            if not match.empty:
                Rebar_Diameter = match.iloc[0, 1]  
                Rebar_area = match.iloc[0, 2]  
            else:
                print("The rebar size you typed is not in our list of rebar sizes.")
                sys.exit()
            As = Top_Rebar_Count*Rebar_area + Bottom_Rebar_Count*Rebar_area
            print("As = " + str(Top_Rebar_Count) + "*" + str(Rebar_area) + " + " + str(Top_Rebar_Count) + "*" + str(Rebar_area) + " = " + str(As) + " in^2")
            #Finding c and a
            if fpc <= 4000:
                print("f'c ≤ 4000 so β1 = 0.85")
                beta1 = 0.85
            elif fpc >= 8000:
                print("f'c ≥ 8000 so β1 = 0.65")
                beta1 = 0.65
            else:
                print("4000 ≤ f'c ≤ 8000")
                beta1 = 0.85 - (0.05*(fpc-4000)/1000)
                print("β1 = 0.85-0.05(f'c-4000)/1000     0.85-0.05(" + str(fpc) + "-4000)/1000 = " + str(round(beta1,3)))
            c = As*fy*1000/(0.85*fpc*beta1*b)
            print("c = As*fy*1000/(0.85*f'c*β1*b)     " + str(As) + "*" + str(fy) + "*1000/(0.85*" + str(fpc) + "*" + str(round(beta1,3)) + "*" + str(b) + ") = " + str(round(c,3)) + " in")
            a = beta1*c
            print("a = β1*c     " + str(round(beta1,3)) + "*" + str(round(c,3)) + " = " + str(round(a,3)) + " in")
            # checking flexural steel
            ecu = 0.003
            print("εcu = 0.003")
            es = ecu*(d1-c)/c
            print("εs = εcu(d1-c)/c     " + str(ecu) + "(" + str(d1) + "-" + str(round(c,3)) + ")/" + str(round(c,3)) + " = " + str(round(es,5)))
            ey = fy/29000
            print("εy = fy/29000     " + str(fy) + "/29000 = " + str(round(ey,5)))
            if es >= ey:
                print("εs = " + str(round(es,5)) + " ≥ εy = " + str(round(ey,5)) + " GOOD")
            else:
                print("εs = " + str(round(es,5)) + " ≥ εy = " + str(round(ey,5)) + " NO, and wont pass Φf = 0.9 since εt ≥ ey + 0.003")
                sys.exit()
                #Note possible it might pass if d is big enough but doutful and at that point probably closer to double reinforced.
                #leaving space and note incase we decide to add it.
                
                
                
                
                
                
            est = ecu*(d2-c)/c
            print("εs = εcu(d2-c)/c     " + str(ecu) + "(" + str(d2) + "-" + str(round(c,3)) + ")/" + str(round(c,3)) + " = " + str(round(est,5)))    
            if est >= ey + 0.003:
                print("εt = " + str(round(est,5)) + " ≥ εy + 0.003 = " + str(round(ey,5)) + " + 0.003 = " + str(round(ey+0.003,5))+ " GOOD")
                print("Therefore Φf = 0.9")
                phif = 0.9
            else:
                print("εt = " + str(round(es,5)) + " ≥ εy + 0.003 = " + str(round(ey,5)) + " + 0.003 = " + str(round(ey+0.003,5))+ " NO")
                print("Fails Φf = 0.9")
                sys.exit()
            # Calculating PhifMn
            d = (d1*Top_Rebar_Count*Rebar_area + d2*Bottom_Rebar_Count*Rebar_area)/(As)
            print("d = (d1*As1+d2*As2)/As     (" + str(d1) + "*" + str(Top_Rebar_Count) + "*" + str(Rebar_area) + "+" + str(d2) + "*" + str(Bottom_Rebar_Count) + "*" + str(Rebar_area) + ")/" + str(As) + " = " + str(round(d,3)) + " in")
            PhifMn = phif*As*fy*(d-a/2)/12
            print("ΦfMn = Φf*As*fy*(d-a/2)/12     " + str(phif) + "*" + str(As) + "*" + str(fy) + "*(" + str(round(d,3)) + "-" + str(round(a,3)) + "/2)/12 = " + str(round(PhifMn,3)) + " kft")
            # Checking Asmin
            Asmin1 = 3*(fpc)**(1/2)/(fy*1000)*b*d
            print("Asmin1 = 3√(fpc)/(fy*1000)*b*d     3√(" + str(fpc) + ")/(" + str(fy) + "*1000)*" + str(b) + "*" + str(round(d,3)) + " = " + str(round(Asmin1,3)) + " in^2")
            Asmin2 = 200/(fy*1000)*b*d
            print("Asmin2 = 200/(fy*1000)*b*d     200/(" + str(fy) + "*1000)*" + str(b) + "*" + str(round(d,3)) + " = " + str(round(Asmin2,3)) + " in^2")
            Asmin = max(Asmin1, Asmin2)
            print("Asmin = " + str(round(Asmin,3)) + " in^2")
            if As >= Asmin:
                print("As = " + str(round(As,3)) + " ≥ Asmin = " + str(round(Asmin,3)) + " GOOD")
            else:
                print("As = " + str(round(As,3)) + " ≥ Asmin = " + str(round(Asmin,3)) + " NO beam fails")

    # code for doubly reinforced beams
    if beam_type == "Doubbly Reinforced":
        Questions = ["f'c (psi)", "b (in)", "h (in)", "Top steel d1 (in)", "Low steel d2 (in)", "fy (ksi)", "Top Rebar Size", "Top Number of Rebar", "Bottom Rebar Size", "Bottom Number of Rebar"]
        if __name__ == '__main__':
            fpc, b, h, d1, d2, fy, Top_Rebar_Size, Top_Rebar_Count, Bottom_Rebar_Size, Bottom_Rebar_Count = get_inputs()
            # finding area of rebar
            df = pd.read_excel('Reinforced_Concrete_Tables.xlsx', sheet_name='Rebar_Size', engine='openpyxl') 
            match = df[df["Bar number"] == Top_Rebar_Size]
            if not match.empty:
                Top_Rebar_Diameter = match.iloc[0, 1]  
                Top_Rebar_area = match.iloc[0, 2]  
            else:
                print("The rebar size you typed is not in our list of rebar sizes.")
                sys.exit()
            match = df[df["Bar number"] == Bottom_Rebar_Size]
            if not match.empty:
                Bottom_Rebar_Diameter = match.iloc[0, 1]  
                Bottom_Rebar_area = match.iloc[0, 2]  
            else:
                print("The rebar size you typed is not in our list of rebar sizes.")
                sys.exit()
            Asp = Top_Rebar_Count*Top_Rebar_area
            print("Asp = " + str(Top_Rebar_Count) + "*" + str(Top_Rebar_area) + " = " + str(Asp) + " in^2")
            As = Bottom_Rebar_Count*Bottom_Rebar_area
            print("As = " + str(Bottom_Rebar_Count) + "*" + str(Bottom_Rebar_area) + " = " + str(As) + " in^2")
            #Finding c and a
            if fpc <= 4000:
                print("f'c ≤ 4000 so β1 = 0.85")
                beta1 = 0.85
            elif fpc >= 8000:
                print("f'c ≥ 8000 so β1 = 0.65")
                beta1 = 0.65
            else:
                print("4000 ≤ f'c ≤ 8000")
                beta1 = 0.85 - (0.05*(fpc-4000)/1000)
                print("β1 = 0.85-0.05(f'c-4000)/1000     0.85-0.05(" + str(fpc) + "-4000)/1000 = " + str(round(beta1,3)))
            c = (As*fy*1000-Asp*(fy*1000-0.85*fpc))/(0.85*fpc*beta1*b)
            print("c = (As*fy*1000-As'(fy-0.85*f'c))/(0.85*f'c*β1*b)     (" + str(As) + "*" + str(fy) + "*1000-" + str(Asp) + "*(" + str(fy) + "*1000-0.85*" + str(fpc) + "))/(0.85*" + str(fpc) + "*" + str(round(beta1,3)) + "*" + str(b) + ") = " + str(round(c,3)) + " in")
            a = beta1*c
            print("a = β1*c     " + str(round(beta1,3)) + "*" + str(round(c,3)) + " = " + str(round(a,3)) + " in")
            #checking if the compression from steel actually is in play
            if(d1<=a):
                # checking flexural steel
                ecu = 0.003
                print("εcu = 0.003")
                es = ecu*(d2-c)/c
                print("εs = εcu(d2-c)/c     " + str(ecu) + "(" + str(d2) + "-" + str(round(c,3)) + ")/" + str(round(c,3)) + " = " + str(round(es,5)))
                ey = fy/29000
                print("εy = fy/29000     " + str(fy) + "/29000 = " + str(round(ey,5)))
                if es >= ey:
                    print("εs = " + str(round(es,5)) + " ≥ εy = " + str(round(ey,5)) + " GOOD")
                else:
                    print("εs = " + str(round(es,5)) + " ≥ εy = " + str(round(ey,5)) + " NO, and wont pass Φf = 0.9 since εt ≥ ey + 0.003")
                    sys.exit()
                esp = ecu*(c-d1)/c
                print("εs' = εcu(c-d1)/c     " + str(ecu) + "(" + str(round(c,3)) + "-" + str(d1) + ")/" + str(round(c,3)) + " = " + str(round(esp,5)))    
                if esp >= ey:
                    print("εs' = " + str(round(esp,5)) + " ≥ εy = " + str(round(ey,5)) + " GOOD")
                    # Calculating PhifMn
                    if es >= ey + 0.003:
                        print("εt = " + str(round(es,5)) + " ≥ εy + 0.003 = " + str(round(ey,5)) + " + 0.003 = " + str(round(ey+0.003,5))+ " GOOD")
                        print("Therefore Φf = 0.9")
                        phif = 0.9
                        PhifMn = phif*((Asp*29000*0.003*(c-d1)/c-Asp*0.85*fpc/1000)*(d2-d1)+0.85*fpc/1000*beta1*c*b*(d2-a/2))/12
                        print("ΦfMn = Φf*((Asp*29000*0.003*(c-d1)/c-Asp*0.85*fpc/1000)*(d2-d1)+0.85*fpc/1000*beta1*c*b*(d2-a/2))/12     " + str(phif) + "*((" + str(Asp) + "*29000*0.003*(" + str(round(c,3)) + "-" + str(d1) + ")/" + str(round(c,3)) + "-" + str(Asp) + "-0.85*" + str(fpc) + "/1000)*(" + str(d2) + "-" + str(d1) + ")+0.85*" + str(fpc) + "/1000*" + str(beta1) + "*" + str(round(c,3)) + "*" + str(b) + "*(" + str(round(d2,3)) + "-" + str(round(a,3)) + "/2))/12 = " + str(round(PhifMn,3)) + " kft")
                    else:
                        print("εt = " + str(round(es,5)) + " ≥ εy + 0.003 = " + str(round(ey,5)) + " + 0.003 = " + str(round(ey+0.003,5))+ " NO")
                        print("Fails Φf = 0.9")
                        sys.exit()
                else:
                    print("εs' = " + str(round(esp,5)) + " ≥ εy = " + str(round(ey,5)) + "NO")
                    # need to add in when top is not equal to es aka need to solve quadratic.
                    print("Quadratic formula")
                    quad_a = 0.85*fpc*beta1*b/1000
                    print("a = 0.85*f'c*β1*b     0.85*" + str(fpc) + "*" + str(beta1) + "*" + str(b) + "/1000 = " + str(round(quad_a,3)))
                    quad_b = (Asp*29000000*0.003-Asp*0.85*fpc-As*fy*1000)/1000
                    print("b = (As'*29000000*0.003-As'*0.85*f'c-As*fy*1000)/1000     (" + str(Asp) + "*29000000*0.003-" + str(Asp) + "*0.85*" + str(fpc) + "-" + str(As) + "*" + str(fy) + "*1000)/1000 = " + str(round(quad_b,3)))
                    quad_c = -Asp*29000*0.003*d1
                    print("c = -As'*29000*0.003*d1     " + str(Asp) + "*29000*0.003*" + str(d1) + " = " + str(round(quad_c,3)))
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
                    #checks
                    a = beta1*c
                    print("a = β1*c     " + str(round(beta1,3)) + "*" + str(round(c,3)) + " = " + str(round(a,3)) + " in")
                    if(d1<=a):
                        # checking flexural steel
                        ecu = 0.003
                        print("εcu = 0.003")
                        es = ecu*(d2-c)/c
                        print("εs = εcu(d2-c)/c     " + str(ecu) + "(" + str(d2) + "-" + str(round(c,3)) + ")/" + str(round(c,3)) + " = " + str(round(es,5)))
                        ey = fy/29000
                        print("εy = fy/29000     " + str(fy) + "/29000 = " + str(round(ey,5)))
                        if es >= ey:
                            print("εs = " + str(round(es,5)) + " ≥ εy = " + str(round(ey,5)) + " GOOD")
                        else:
                            print("εs = " + str(round(es,5)) + " ≥ εy = " + str(round(ey,5)) + " NO, and wont pass Φf = 0.9 since εt ≥ ey + 0.003")
                            sys.exit()
                        esp = ecu*(c-d1)/c
                        print("εs' = εcu(c-d1)/c     " + str(ecu) + "(" + str(round(c,3)) + "-" + str(d1) + ")/" + str(round(c,3)) + " = " + str(round(esp,5)))    
                        if esp < ey:
                            print("εs' = " + str(round(esp,5)) + " < εy = " + str(round(ey,5)) + " GOOD")
                            # Calculating PhifMn
                            if es >= ey + 0.003:
                                print("εt = " + str(round(es,5)) + " ≥ εy + 0.003 = " + str(round(ey,5)) + " + 0.003 = " + str(round(ey+0.003,5))+ " GOOD")
                                print("Therefore Φf = 0.9")
                                phif = 0.9
                                PhifMn = phif*((Asp*29000*0.003*(c-d1)/c-Asp*0.85*fpc/1000)*(d2-d1)+0.85*fpc/1000*beta1*c*b*(d2-a/2))/12
                                print("ΦfMn = Φf*((Asp*29000*0.003*(c-d1)/c-Asp*0.85*fpc/1000)*(d2-d1)+0.85*fpc/1000*beta1*c*b*(d2-a/2))/12     " + str(phif) + "*((" + str(Asp) + "*29000*0.003*(" + str(round(c,3)) + "-" + str(d1) + ")/" + str(round(c,3)) + "-" + str(Asp) + "-0.85*" + str(fpc) + "/1000)*(" + str(d2) + "-" + str(d1) + ")+0.85*" + str(fpc) + "/1000*" + str(beta1) + "*" + str(round(c,3)) + "*" + str(b) + "*(" + str(round(d2,3)) + "-" + str(round(a,3)) + "/2))/12 = " + str(round(PhifMn,3)) + " kft")
                            else:
                                print("εt = " + str(round(es,5)) + " ≥ εy + 0.003 = " + str(round(ey,5)) + " + 0.003 = " + str(round(ey+0.003,5))+ " NO")
                                print("Fails Φf = 0.9")
                                sys.exit()
                        else:
                            print("An error occured and top strain never works, sorry for the inconvienence.")
                            sys.exit()
                    else:
                        c = As*fy*1000/(0.85*fpc*beta1*b)
                        print("c = As*fy*1000/(0.85*f'c*β1*b)     " + str(As) + "*" + str(fy) + "*1000/(0.85*" + str(fpc) + "*" + str(round(beta1,3)) + "*" + str(b) + ") = " + str(round(c,3)) + " in")
                        a = beta1*c
                        print("a = β1*c     " + str(round(beta1,3)) + "*" + str(round(c,3)) + " = " + str(round(a,3)) + " in")
                        # checking flexural steel
                        ecu = 0.003
                        print("εcu = 0.003")
                        es = ecu*(d2-c)/c
                        print("εs = εcu(d2-c)/c     " + str(ecu) + "(" + str(d2) + "-" + str(round(c,3)) + ")/" + str(round(c,3)) + " = " + str(round(es,5)))
                        ey = fy/29000
                        print("εy = fy/29000     " + str(fy) + "/29000 = " + str(round(ey,5)))
                        if es >= ey:
                            print("εs = " + str(round(es,5)) + " ≥ εy = " + str(round(ey,5)) + " GOOD")
                        else:
                            print("εs = " + str(round(es,5)) + " ≥ εy = " + str(round(ey,5)) + " NO, and wont pass Φf = 0.9 since εt ≥ ey + 0.003")
                            sys.exit()
                        if es >= ey + 0.003:
                            print("εt = " + str(round(es,5)) + " ≥ εy + 0.003 = " + str(round(ey,5)) + " + 0.003 = " + str(round(ey+0.003,5))+ " GOOD")
                            print("Therefore Φf = 0.9")
                            phif = 0.9
                        else:
                            print("εt = " + str(round(es,5)) + " ≥ εy + 0.003 = " + str(round(ey,5)) + " + 0.003 = " + str(round(ey+0.003,5))+ " NO")
                            print("Fails Φf = 0.9")
                            sys.exit()
                        # Calculating PhifMn
                        PhifMn = phif*As*fy*(d2-a/2)/12
                        print("ΦfMn = Φf*As*fy*(d2-a/2)/12     " + str(phif) + "*" + str(As) + "*" + str(fy) + "*(" + str(d2) + "-" + str(round(a,3)) + "/2)/12 = " + str(round(PhifMn,3)) + " kft")    
            else:
                c = As*fy*1000/(0.85*fpc*beta1*b)
                print("c = As*fy*1000/(0.85*f'c*β1*b)     " + str(As) + "*" + str(fy) + "*1000/(0.85*" + str(fpc) + "*" + str(round(beta1,3)) + "*" + str(b) + ") = " + str(round(c,3)) + " in")
                a = beta1*c
                print("a = β1*c     " + str(round(beta1,3)) + "*" + str(round(c,3)) + " = " + str(round(a,3)) + " in")
                # checking flexural steel
                ecu = 0.003
                print("εcu = 0.003")
                es = ecu*(d2-c)/c
                print("εs = εcu(d2-c)/c     " + str(ecu) + "(" + str(d2) + "-" + str(round(c,3)) + ")/" + str(round(c,3)) + " = " + str(round(es,5)))
                ey = fy/29000
                print("εy = fy/29000     " + str(fy) + "/29000 = " + str(round(ey,5)))
                if es >= ey:
                    print("εs = " + str(round(es,5)) + " ≥ εy = " + str(round(ey,5)) + " GOOD")
                else:
                    print("εs = " + str(round(es,5)) + " ≥ εy = " + str(round(ey,5)) + " NO, and wont pass Φf = 0.9 since εt ≥ ey + 0.003")
                    sys.exit()
                if es >= ey + 0.003:
                    print("εt = " + str(round(es,5)) + " ≥ εy + 0.003 = " + str(round(ey,5)) + " + 0.003 = " + str(round(ey+0.003,5))+ " GOOD")
                    print("Therefore Φf = 0.9")
                    phif = 0.9
                else:
                    print("εt = " + str(round(es,5)) + " ≥ εy + 0.003 = " + str(round(ey,5)) + " + 0.003 = " + str(round(ey+0.003,5))+ " NO")
                    print("Fails Φf = 0.9")
                    sys.exit()
                # Calculating PhifMn
                PhifMn = phif*As*fy*(d2-a/2)/12
                print("ΦfMn = Φf*As*fy*(d2-a/2)/12     " + str(phif) + "*" + str(As) + "*" + str(fy) + "*(" + str(d2) + "-" + str(round(a,3)) + "/2)/12 = " + str(round(PhifMn,3)) + " kft")
            # Checking Asmin
            Asmin1 = 3*(fpc)**(1/2)/(fy*1000)*b*d2
            print("Asmin1 = 3√(fpc)/(fy*1000)*b*d2     3√(" + str(fpc) + ")/(" + str(fy) + "*1000)*" + str(b) + "*" + str(d2) + " = " + str(round(Asmin1,3)) + " in^2")
            Asmin2 = 200/(fy*1000)*b*d2
            print("Asmin2 = 200/(fy*1000)*b*d2     200/(" + str(fy) + "*1000)*" + str(b) + "*" + str(d2) + " = " + str(round(Asmin2,3)) + " in^2")
            Asmin = max(Asmin1, Asmin2)
            print("Asmin = " + str(round(Asmin,3)) + " in^2")
            if As >= Asmin:
                print("As = " + str(round(As,3)) + " ≥ Asmin = " + str(round(Asmin,3)) + " GOOD")
            else:
                print("As = " + str(round(As,3)) + " ≥ Asmin = " + str(round(Asmin,3)) + " NO beam fails")
    
    # T or L
    if beam_type == "T or L":
        Questions = ["f'c (psi)", "b of flange (in)", "b of web (in)", "h of flange (in)", "h total (in)", "d (in)", "fy (ksi)", "Rebar Size", "Number of Rebar"]
        if __name__ == '__main__':
            fpc, bf, bw, hf, h, d, fy, Rebar_Size, Rebar_Count = get_inputs()
        question = "Positive or Negative Moment"
        options = ["Positive", "Negative"]
        if __name__ == "__main__":
            moment_direction = choice(question, options)
        if moment_direction == "Positive":
            # checking inputs
            if hf >= h:
                print("The height of the flange is bigger or eual to the total height of the beam and that cant be for a T or L.")
                sys.exit()
            if bw > bf:
                print("The width of the web is larger than the flange and that cant be for a T or L.")
                sys.exit()
            # finding area of rebar
            df = pd.read_excel('Reinforced_Concrete_Tables.xlsx', sheet_name='Rebar_Size', engine='openpyxl') 
            match = df[df["Bar number"] == Rebar_Size]
            if not match.empty:
                Rebar_Diameter = match.iloc[0, 1]  
                Rebar_area = match.iloc[0, 2]  
            else:
                print("The rebar size you typed is not in our list of rebar sizes.")
                sys.exit()
            As = Rebar_Count*Rebar_area
            print("As = " + str(Rebar_Count) + "*" + str(Rebar_area) + " = " + str(As) + " in^2")
            #Finding c and a
            if fpc <= 4000:
                print("f'c ≤ 4000 so β1 = 0.85")
                beta1 = 0.85
            elif fpc >= 8000:
                print("f'c ≥ 8000 so β1 = 0.65")
                beta1 = 0.65
            else:
                print("4000 ≤ f'c ≤ 8000")
                beta1 = 0.85 - (0.05*(fpc-4000)/1000)
                print("β1 = 0.85-0.05(f'c-4000)/1000     0.85-0.05(" + str(fpc) + "-4000)/1000 = " + str(round(beta1,3)))
            c = As*fy*1000/(0.85*fpc*beta1*bw)
            print("c = As*fy*1000/(0.85*f'c*β1*bw)     " + str(As) + "*" + str(fy) + "*1000/(0.85*" + str(fpc) + "*" + str(round(beta1,3)) + "*" + str(bw) + ") = " + str(round(c,3)) + " in")
            a = beta1*c
            print("a = β1*c     " + str(round(beta1,3)) + "*" + str(round(c,3)) + " = " + str(round(a,3)) + " in")
            #checking hf vs a
            if a > hf:
                print("a > hf therefor diffrent eq for c")
                c = (As*fy*1000-0.85*fpc*(bf-bw)*hf)/(0.85*fpc*beta1*bw)
                print("c = (As*fy*1000-0.85*f'c*(bf-bw)*hf)/(0.85*f'c*β1*bw)     (" + str(As) + "*" + str(fy) + "*1000-0.85*" + str(fpc) + "*(" + str(bf) + "-" + str(bw) + ")*" + str(hf) + ")/(0.85*" + str(fpc) + "*" + str(round(beta1,3)) + "*" + str(bw) + ") = " + str(round(c,3)) + " in")
                a = beta1*c
                print("a = β1*c     " + str(round(beta1,3)) + "*" + str(round(c,3)) + " = " + str(round(a,3)) + " in")
                if a <= hf:
                    print("An error has occured when finding c sorry for the inconvienence.")
                    sys.exit()
            # checking flexural steel
            ecu = 0.003
            print("εcu = 0.003")
            es = ecu*(d-c)/c
            print("εs = εcu(d-c)/c     " + str(ecu) + "(" + str(d) + "-" + str(round(c,3)) + ")/" + str(round(c,3)) + " = " + str(round(es,5)))
            ey = fy/29000
            print("εy = fy/29000     " + str(fy) + "/29000 = " + str(round(ey,5)))
            if es >= ey:
                print("εs = " + str(round(es,5)) + " ≥ εy = " + str(round(ey,5)) + " GOOD")
            else:
                print("εs = " + str(round(es,5)) + " ≥ εy = " + str(round(ey,5)) + " NO, and wont pass Φf = 0.9 since εt ≥ ey + 0.003")
                sys.exit()
            if es >= ey + 0.003:
                print("εt = " + str(round(es,5)) + " ≥ εy + 0.003 = " + str(round(ey,5)) + " + 0.003 = " + str(round(ey+0.003,5))+ " GOOD")
                print("Therefore Φf = 0.9")
                phif = 0.9
            else:
                print("εt = " + str(round(es,5)) + " ≥ εy + 0.003 = " + str(round(ey,5)) + " + 0.003 = " + str(round(ey+0.003,5))+ " NO")
                print("Fails Φf = 0.9")
                sys.exit()
            # Calculating PhifMn
            if a <= hf:
                PhifMn = phif*As*fy*(d-a/2)/12
                print("ΦfMn = Φf*As*fy*(d-a/2)/12     " + str(phif) + "*" + str(As) + "*" + str(fy) + "*(" + str(d) + "-" + str(round(a,3)) + "/2)/12 = " + str(round(PhifMn,3)) + " kft")
            else:
                PhifMn = phif*(0.85*fpc*(bf-bw)*hf*(d-hf/2)+0.85*fpc*a*bw*(d-a/2))/(12*1000)
                print("ΦfMn = Φf*(0.85*f'c*(bf-bw)*hf*(d-hf/2)+0.85*f'c*a*bw*(d-a/2))/(12*1000)     " + str(phif) + "*(0.85*" + str(fpc) + "*(" + str(bf) + "-" + str(bw) + ")*" + str(hf) + "*(" + str(d) + "-" + str(hf) + ")+0.85*" + str(fpc) + "*" + str(a) + "*" + str(bw) + "*(" + str(d) + "-" + str(a) + "/2))/(12*1000) = " + str(round(PhifMn,3)))
            # Checking Asmin
            Asmin1 = 3*(fpc)**(1/2)/(fy*1000)*bw*d
            print("Asmin1 = 3√(fpc)/(fy*1000)*bw*d     3√(" + str(fpc) + ")/(" + str(fy) + "*1000)*" + str(bw) + "*" + str(d) + " = " + str(round(Asmin1,3)) + " in^2")
            Asmin2 = 200/(fy*1000)*bw*d
            print("Asmin2 = 200/(fy*1000)*bw*d     200/(" + str(fy) + "*1000)*" + str(bw) + "*" + str(d) + " = " + str(round(Asmin2,3)) + " in^2")
            Asmin = max(Asmin1, Asmin2)
            print("Asmin = " + str(round(Asmin,3)) + " in^2")
            if As >= Asmin:
                print("As = " + str(round(As,3)) + " ≥ Asmin = " + str(round(Asmin,3)) + " GOOD")
            else:
                print("As = " + str(round(As,3)) + " ≥ Asmin = " + str(round(Asmin,3)) + " NO Beam fails")
        elif moment_direction == "Negative":
            print("Yet to be coded.")







    if beam_type == "Shear":
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
    #deflection
    if beam_type == "Deflection":
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


# desgin start
elif procedure == "Desgining":
    # Which version of a beam
    question = "What type of beam"
    options = ["Singely Reinforced Known Dimensions","Singely Reinforced Unknown Dimensions"]
    if __name__ == "__main__":
        beam_type = choice(question, options)
    # Asking for all required values
    if beam_type == "Singely Reinforced Known Dimensions":
        Questions = ["f'c (psi)", "b (in)", "h (in)", "fy (ksi)", "Aggergate size", "Mu (kft)", "Stirrup Leg Size", "Number of legs"]
        if __name__ == '__main__':
            fpc, b, h, fy, dagg, Mu, Stirrup_size, Legs = get_inputs()
        question = "What type of exposure"
        options = ["No exposure to weather or ground", "Exposed to weather or ground", "Cast against and constant contact with ground"]
        if __name__ == "__main__":
            exposure = choice(question, options)
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
        #quick overview
        for i in range(len(flexure_rebar)):
            print("dc_ratio of " + str(num_of_bars[i]) + " #" + str(flexure_rebar[i]) + "bars: " + str(round(dc_ratio[i],3)))
                        
                        
                        
                        
                        
                    























