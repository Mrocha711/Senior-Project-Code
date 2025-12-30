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
                beta1 = 0.85 - (0.05(fpc-4000)/1000)
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
                beta1 = 0.85 - (0.05(fpc-4000)/1000)
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
                print("εt = " + str(round(es,5)) + " ≥ εy + 0.003 = " + str(round(ey,5)) + " + 0.003 = " + str(round(ey+0.003,5))+ " GOOD")
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
                beta1 = 0.85 - (0.05(fpc-4000)/1000)
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
                beta1 = 0.85 - (0.05(fpc-4000)/1000)
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
            fpc, b, h, d, cover, flex_Rebar_Size, bar_number, fyt, Shear_Rebar_Size, Bands, Stirrup_legs, Lt, Nu, w = get_inputs()
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
        if w <= 100:
            print("w ≤ 100     " + str(w) + " ≤ 100 Therefore λ = 0.75")
            lam = 0.75
        elif w >= 135:
            print("w ≥ 135     " + str(w) + " ≤ 135 Therefore λ = 1")
            lam = 1
        else:
            lam = 0.0075*w
            print("100 < w < 135     100 < " + str(w) + " < 135 Therefore λ = 0.0075*w     0.0075*" + str(w) + " = " + str(lam))
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
        if rebar_shape == "Singly Reinforced":
            Questions = ["f'c (psi)", "b (in)", "h (in)", "d (in)", "Rebar size", "Number of bars", "fy (ksi)", "Length (ft)", "weight of concrete (pcf)"]
            if __name__ == '__main__':
                fpc, b, h, d, Low_Rebar_Size, Low_Number_Bars, fy, L, w = get_inputs()
        elif rebar_shape == "Doubly Reinforced":
            Questions = ["f'c (psi)", "b (in)", "h (in)", "Upper d (in)", "Upper Rebar size", "Upper Number of bars", "Low d (in)", "Low Rebar size", "Low Number of bars", "fy (ksi)", "Length (ft)", "weight of concrete (pcf)"]
            if __name__ == '__main__':
                fpc, b, h, d1, Up_Rebar_Size, Up_Number_Bars, d2, Low_Rebar_Size, Low_Number_Bars, fy, L, w = get_inputs()
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
        # moments of inertia calcs
        Ig = 1/12*b*h**3
        print("Ig = 1/12*b*h^3     1/12*" + str(b) + "*" + str(h) + "^3 = " + str(Ig) + " in^4")
        Ec = w**1.5*33*fpc**0.5/1000
        print("Ec = w^1.5*33*√(f'c)/1000     " + str(w) + "^1.5*33*√(" + str(fpc) + ")/1000 = " + str(round(Ec,3)) + " ksi")
        n = 29000/Ec
        print("n = Es/Ec     29000/" + str(round(Ec,3)) + " = " + str(round(n,3)))
        
        
        
        
        
        
        
        
        
        







