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
            As = round(Top_Rebar_Count*Rebar_area + Bottom_Rebar_Count*Rebar_area,2)
            print("As = " + str(Top_Rebar_Count) + "*" + str(Rebar_area) + " + " + str(Bottom_Rebar_Count) + "*" + str(Rebar_area) + " = " + str(As) + " in^2")
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
                print("εt = " + str(round(est,5)) + " ≥ εy + 0.003 = " + str(round(ey,5)) + " + 0.003 = " + str(round(ey+0.003,5))+ " NO")
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
            w_d = 0
            w_l = 0 
    elif load == "distributed load":
        Questions = ["What is the dead distributed load (k/ft)", "What is the live distributed load (k/ft)",  "Live Load percent sustained (%)", "Time dependent Factor"]
        if __name__ == '__main__':
            w_d, w_l, percent, zata_s = get_inputs()
            P_d = 0
            P_l = 0  
    # this variable is just here to make printing easier and more controllable
    design_math_1 = ""
    if beam_type == "Singely Reinforced Known Dimensions":
        Questions = ["f'c (psi)", "b (in)", "h (in)", "fy (ksi)", "Nu (k)", "Length of beam (ft)", "Aggergate size", "Weight of Concrete pcf", "fyt (ksi)", "Stirrup Leg Size", "Number of legs"]
        if __name__ == '__main__':
            fpc, b, h, fy, Nu, L, dagg, wc, fyt, Stirrup_size, Legs = get_inputs()
    elif beam_type == "Singely Reinforced Unknown Dimensions":
        Questions = ["f'c (psi)", "fy (ksi)", "Nu (k)", "Length of beam (ft)", "Aggergate size", "Weight of Concrete pcf", "fyt (ksi)", "Stirrup Leg Size", "Number of legs"]
        if __name__ == '__main__':
            fpc, fy, Nu, L, dagg, wc, fyt, Stirrup_size, Legs = get_inputs()
        #solving for trial size
        if B_type == "Simply Supported":
            h = L*12/16
            design_math_1 += "\nSince Simply supported min h = L*12/16     " + str(L) + "*12/16 = " + str(h) + " in"
        elif B_type == "Cantilever":
            h = L*12/8
            design_math_1 += "\nSince Simply supported min h = L*12/8     " + str(L) + "*12/8 = " + str(h) + " in"
        b = 0.8*h 
        design_math_1 += "\nb = 0.8h     0.8" + str(h) + " = " + str(b) + " in"
        wg = b/12*h/12*wc/1000
        design_math_1 += "\nwg = b/12*h/12*wc/1000     " + str(b) + "/12*" + str(h) + "/12*" + str(wc) + "/1000 = " + str(wg) + "klf"
        #finding trial max Mu
        w_trial_1 = 1.4*(w_d+wg)
        design_math_1 += "\nw_trial_1 = 1.4*(w_d+wg)     1.4*(" + str(wg) + "+" + str(w_d) + ") = " + str(w_trial_1) + "klf"
        P_trial_1 = 1.4*P_d
        design_math_1 += "\nP_trial_1 = 1.4*P_d     1.4*" + str(P_d) + " = " + str(P_trial_1) + " k"
        w_trial_2 = 1.2*(w_d+wg)+1.6*w_l
        design_math_1 += "\nw_trial_2 = 1.2*(w_d+wg)+1.6*w_l     1.2*(" + str(wg) + "+" + str(w_d) + ") + 1.6*" + str(w_l) + " = " + str(w_trial_2) + "klf"
        P_trial_2 = 1.2*P_d+1.6*P_l
        design_math_1 += "\nP_trial_1 = 1.2*P_d+1.6*P_l     1.2*" + str(P_d) + "+1.6*" + str(P_l) + " = " + str(P_trial_2) + " k"
        if B_type == "Simply Supported":
            M_trial_1 = w_trial_1*L**2/8+P_trial_1*L/4
            design_math_1 += "\nM_trial_1 = w_trial_1*L^2/8+P_trial_1*L/4     " + str(w_trial_1) + "*" + str(L) + "^2/8+" + str(P_trial_1) + "*" + str(L) + "/4 = " + str(M_trial_1) + " kft"
            M_trial_2 = w_trial_2*L**2/8+P_trial_2*L/4
            design_math_1 += "\nM_trial_2 = w_trial_2*L^2/8+P_trial_2*L/4     " + str(w_trial_2) + "*" + str(L) + "^2/8+" + str(P_trial_2) + "*" + str(L) + "/4 = " + str(M_trial_2) + " kft"
        elif B_type == "Cantilever":
            M_trial_1 = w_trial_1*L**2/2+P_trial_1*L
            design_math_1 += "\nM_trial_1 = w_trial_1*L**2/2+P_trial_1*L     " + str(w_trial_1) + "*" + str(L) + "^2/2+" + str(P_trial_1) + "*" + str(L) + " = " + str(M_trial_1) + " kft"
            M_trial_2 = w_trial_2*L**2/2+P_trial_2*L
            design_math_1 += "\nM_trial_2 = w_trial_2*L**2/2+P_trial_2*L     " + str(w_trial_2) + "*" + str(L) + "^2/2+" + str(P_trial_2) + "*" + str(L) + " = " + str(M_trial_2) + " kft"
        M_trial = max(M_trial_1,M_trial_2)
        design_math_1 += "\nM_trial = " + str(M_trial) + " kft"
        if fpc <= 4000:
            design_math_1 += "\nf'c ≤ 4000 so β1 = 0.85"
            beta1 = 0.85
        elif fpc >= 8000:
            design_math_1 += "\nf'c ≥ 8000 so β1 = 0.65"
            beta1 = 0.65
        else:
            design_math_1 += "\n4000 ≤ f'c ≤ 8000"
            beta1 = 0.85 - (0.05*(fpc-4000)/1000)
            design_math_1 += "\nβ1 = 0.85-0.05(f'c-4000)/1000     0.85-0.05(" + str(fpc) + "-4000)/1000 = " + str(round(beta1,3))
        rho_trial =  beta1*fpc/(4*fy*1000)
        design_math_1 += "\nρ_trial =  β1*f'c/(4*fy*1000)     " + str(beta1) + "*" + str(fpc) + "/(4*" + str(fy) + "*1000) = " + str(rho_trial)   
        omega = rho_trial*fy*1000/fpc
        design_math_1 += "\nω = ρ_trial*1000*fy/f'c     " + str(rho_trial) + "*1000*" + str(fy) + "/" + str(fpc) + " = " + str(omega)
        R = omega*fpc/1000*(1-0.59*omega)
        design_math_1 += "\nR = ω*f'c/1000*(1-0.59*ω)     " + str(omega) + "*" + str(fpc) + "/1000*(1-0.59*" + str(omega) + ") = " + str(R)
        d_for_h = (M_trial*12/(0.7*0.9*R))**(1/3)
        design_math_1 += "\nd = (M_u*12/(0.7*ϕ_f*R))^(1/3)     (" + str(M_trial) + "*12/(0.7*0.9*" + str(R) + "))^(1/3) = " + str(d_for_h) + " in"
        b = M_trial*12/(0.9*R*d_for_h**2)
        design_math_1 += "\nb = M_u*12/(ϕ_f*R*d^2)     " + str(M_trial) + "*12/(0.9*" + str(R) + "*" + str(d_for_h) + "^2) = " + str(b) + " in"
        b = round(b+0.5)
        design_math_1 += "\nb rounded to the nearest inch is " + str(b)
        h = d_for_h + 3
        design_math_1 += "\nh = d+3     " + str(d_for_h) + "+3 = " + str(h) + " in"
        h = round(h+0.5)
        design_math_1 += "\nh rounded to the nearest inch is " + str(h)
        wg = b/12*h/12*wc/1000
        design_math_1 += "\nwg = b/12*h/12*wc/1000     " + str(b) + "/12*" + str(h) + "/12*" + str(wc) + "/1000 = " + str(wg) + "klf"
        w_d_tot = w_d+wg
        design_math_1 += "\nw_d = w_d+w_g     " + str(w_d) + "+" + str(wg) + " = " + str(w_d_tot) + " klf"
        w_d = w_d_tot
    # finding values of Vu,Mu, and partial deflection
    if B_type == "Simply Supported":
        if load == "point load" and beam_type == "Singely Reinforced Known Dimensions":
            # load combos
            P1 = 1.6*P_d
            design_math_1 += "\nP1 = 1.6D     1.6*" + str(P_d) + " = " + str(P1) + " kips"
            P2 = 1.2*P_d+1.4*P_l
            design_math_1 += "\nP1 = 1.2D+1.4L     1.2*" + str(P_d) + "1.4*" + str(P_l) + " = " + str(P2) + " kips"
            P = max(P1,P2)
            design_math_1 += "\nTherefor use P = " + str(P) + " kips"
            # solving
            Vu = P/2
            design_math_1 += "\nVu = P/2     " + str(P) + "/2 = " + str(Vu) + " kips"
            Mu = P*L/4
            design_math_1 += "\nMu = PL/4     " + str(P) + "*" + str(L) + "/4 = " + str(Mu) + " kip ft"
            design_math_1 += "\nΔ*EI = P*(L*12)^3/(48)"
            del_iD_EI = P_d*(L*12)**3/(48)
            design_math_1 += "\nΔ_iD*EI = " + str(P_d) + "*(" + str(L) + "*12)^3/(48) = " + str(round(del_iD_EI,3))
            del_iD_L_EI = (P_d+P_l)*(L*12)**3/(48)
            design_math_1 += "\nΔ_iD_L*EI = (" + str(P_d) + "+" + str(P_l) + ")*(" + str(L) + "*12)^3/(48) = " + str(round(del_iD_L_EI,3))
        elif load == "distributed load":
            # load combos
            W1 = 1.6*w_d
            design_math_1 += "\nW1 = 1.6D     1.6*" + str(w_d) + " = " + str(W1) + " kips"
            W2 = 1.2*w_d+1.4*w_l
            design_math_1 += "\nW1 = 1.2D+1.4L     1.2*" + str(w_d) + "1.4*" + str(w_l) + " = " + str(W2) + " kips"
            W = max(W1,W2)
            design_math_1 += "\nTherefor use W = " + str(W) + " kips"
            # solving
            Vu = W*L/2
            design_math_1 += "\nVu = WL/2     " + str(W) + "*" + str(L) + "/2 = " + str(Vu) + " kip"
            Mu = W*L**2/8
            design_math_1 += "\nMu = WL^2/8     " + str(W) + "*" + str(L) + "^2/8 = " + str(Mu) + " kip ft"
            design_math_1 += "\nΔ*EI = 5*w*L^4*12^3/(384)"
            del_iD_EI = 5*w_d*L**4*12**3/(384)
            design_math_1 += "\nΔ_iD*EI = 5*" + str(w_d) + "*" + str(L) + "^4*12^3/(384) = " + str(round(del_iD_EI,3))
            del_iD_L_EI = 5*(w_d+w_l)*L**4*12**3/(384)
            design_math_1 += "\nΔ_iD_L*EI = 5*(" + str(w_d) + "+" + str(w_l) + ")*" + str(L) + "^4*12^3/(384) = " + str(round(del_iD_L_EI,3))
            P = 0
        elif load == "point load" and beam_type == "Singely Reinforced Unknown Dimensions":
            #finding Mu for both cases then getting max Mu
            W1 = 1.4*w_d
            design_math_1 += "\nW1 = 1.4*(w_d)     1.4*(" + str(wg) + ") = " + str(W1) + "klf"
            P1 = 1.4*P_d
            design_math_1 += "\nP1 = 1.4*P_d     1.4*" + str(P_d) + " = " + str(P1) + " k"
            W2 = 1.2*(w_d)+1.6*w_l
            design_math_1 += "\nW2 = 1.2*(w_d)+1.6*w_l     1.2*(" + str(wg) + ") + 1.6*" + str(w_l) + " = " + str(W2) + "klf"
            P2 = 1.2*P_d+1.6*P_l
            design_math_1 += "\nP2 = 1.2*P_d+1.6*P_l     1.2*" + str(P_d) + "+1.6*" + str(P_l) + " = " + str(P2) + " k"
            M1 = W1*L**2/8+P1*L/4
            design_math_1 += "\nM1 = W1*L^2/8+P1*L/4     " + str(W1) + "*" + str(L) + "^2/8+" + str(P1) + "*" + str(L) + "/4 = " + str(M1) + " kft"
            M2 = W2*L**2/8+P2*L/4
            design_math_1 += "\nM2 = W2*L^2/8+P2*L/4     " + str(W2) + "*" + str(L) + "^2/8+" + str(P2) + "*" + str(L) + "/4 = " + str(M2) + " kft"
            Mu = max(M1,M2)
            if Mu == M1:
                Vu = W1*L/2 + P1/2
                P = P1
                W = W1
            else:
                Vu = W2*L/2 + P2/2
                P = P2
                W = W2
            design_math_1 += "\nΔ*EI = 5*w*L^4*12^3/(384)+P*(L*12)^3/(48)"
            del_iD_EI = 5*w_d*L**4*12**3/(384) + P_d*(L*12)**3/(48)
            design_math_1 += "\nΔ_iD*EI = 5*" + str(w_d) + "*" + str(L) + "^4*12^3/(384)+" + str(P_d) + "*(" + str(L) + "*12)^3/(48)= " + str(round(del_iD_EI,3))
            del_iD_L_EI = 5*(w_d+w_l)*L**4*12**3/(384)+(P_d+P_l)*(L*12)**3/(48)
            design_math_1 += "\nΔ_iD_L*EI = 5*(" + str(w_d) + "+" + str(w_l) + ")*" + str(L) + "^4*12^3/(384)+(" + str(P_d) + "+" + str(P_l) + ")*(" + str(L) + "*12)^3/(48) = " + str(round(del_iD_L_EI,3))
    elif B_type == "Cantilever":
        if load == "point load" and beam_type == "Singely Reinforced Known Dimensions":
            # load combos
            P1 = 1.6*P_d
            design_math_1 += "\nP1 = 1.6D     1.6*" + str(P_d) + " = " + str(P1) + " kips"
            P2 = 1.2*P_d+1.4*P_l
            design_math_1 += "\nP1 = 1.2D+1.4L     1.2*" + str(P_d) + "1.4*" + str(P_l) + " = " + str(P2) + " kips"
            P = max(P1,P2)
            design_math_1 += "\nTherefor use P = " + str(P) + " kips"
            # solving
            Vu = P
            design_math_1 += "\nVu = P = " + str(P) + " kips"
            Mu = P*L
            design_math_1 += "\nMu = PL     " + str(P) + "*" + str(L) + " = " + str(Mu) + " kip ft"
            design_math_1 += "\nΔ*EI = P*(L*12)^3/(3)"
            del_iD_EI = P_d*(L*12)**3/(3)
            design_math_1 += "\nΔ_iD*EI = " + str(P_d) + "*(" + str(L) + "*12)^3/(3) = " + str(round(del_iD_EI,3)) + " in"
            del_iD_L_EI = (P_d+P_l)*(L*12)**3/(3)
            design_math_1 += "\nΔ_iD_L*EI = (" + str(P_d) + "+" + str(P_l) + ")*(" + str(L) + "*12)^3/(3) = " + str(round(del_iD_L_EI,3)) + " in"
        elif load == "distributed load":
            W1 = 1.6*w_d
            design_math_1 += "\nW1 = 1.6D     1.6*" + str(w_d) + " = " + str(W1) + " kips"
            W2 = 1.2*w_d+1.4*w_l
            design_math_1 += "\nW1 = 1.2D+1.4L     1.2*" + str(w_d) + "1.4*" + str(w_l) + " = " + str(W2) + " kips"
            W = max(W1,W2)
            design_math_1 += "\nTherefor use W = " + str(W) + " kips"
            # solving
            Vu = W*L
            design_math_1 += "\nVu = WL     " + str(W) + "*" + str(L) + " = " + str(Vu) + " kip"
            Mu = W*L**2/2
            design_math_1 += "\nMu = WL^2/2     " + str(W) + "*" + str(L) + "^2/2 = " + str(Mu) + " kip ft"
            design_math_1 += "\nΔ*EI = w*L^4*12^3/(8)"
            del_iD_EI = w_d*L**4*12**3/(8)
            design_math_1 += "\nΔ_iD*EI = " + str(w_d) + "*" + str(L) + "^4*12^3/(8) = " + str(round(del_iD_EI,3)) + " in"
            del_iD_L_EI = (w_d+w_l)*L**4*12**3/(8)
            design_math_1 += "\nΔ_iD_L*EI = (" + str(w_d) + "+" + str(w_l) + ")*" + str(L) + "^4*12^3/(8) = " + str(round(del_iD_L_EI,3)) + " in"
            P = 0
        elif load == "point load" and beam_type == "Singely Reinforced Unknown Dimensions":
            #finding Mu for both cases then getting max Mu
            W1 = 1.4*w_d
            design_math_1 += "\nW1 = 1.4*(w_d)     1.4*(" + str(wg) + ") = " + str(W1) + "klf"
            P1 = 1.4*P_d
            design_math_1 += "\nP1 = 1.4*P_d     1.4*" + str(P_d) + " = " + str(P1) + " k"
            W2 = 1.2*(w_d)+1.6*w_l
            design_math_1 += "\nW2 = 1.2*(w_d)+1.6*w_l     1.2*(" + str(wg) + ") + 1.6*" + str(w_l) + " = " + str(W2) + "klf"
            P2 = 1.2*P_d+1.6*P_l
            design_math_1 += "\nP2 = 1.2*P_d+1.6*P_l     1.2*" + str(P_d) + "+1.6*" + str(P_l) + " = " + str(P2) + " k"
            M1 = W1*L**2/2+P1*L
            design_math_1 += "\nM1 = W1*L^2/2+P1*L     " + str(W1) + "*" + str(L) + "^2/2+" + str(P1) + "*" + str(L) + " = " + str(M1) + " kft"
            M2 = W2*L**2/2+P2*L
            design_math_1 += "\nM2 = W2*L^2/8+P2*L/4     " + str(W2) + "*" + str(L) + "^2/2+" + str(P2) + "*" + str(L) + " = " + str(M2) + " kft"
            Mu = max(M1,M2)
            if Mu == M1:
                Vu = W1*L/2 + P1/2
                P = P1
                W = W1
            else:
                Vu = W2*L/2 + P2/2
                P = P2
                W = W2
            design_math_1 += "\nΔ*EI = w*L^4*12^3/(8)+P*(L*12)^3/(3)"
            del_iD_EI = w_d*L**4*12**3/(8)+P_d*(L*12)**3/(3)
            design_math_1 += "\nΔ_iD*EI = " + str(w_d) + "*" + str(L) + "^4*12^3/(8)+" + str(P_d) + "*(" + str(L) + "*12)^3/(3) = " + str(round(del_iD_EI,3)) + " in"
            del_iD_L_EI = (w_d+w_l)*L**4*12**3/(8)+(P_d+P_l)*(L*12)**3/(3)
            design_math_1 += "\nΔ_iD_L*EI = (" + str(w_d) + "+" + str(w_l) + ")*" + str(L) + "^4*12^3/(8)+(" + str(P_d) + "+" + str(P_l) + ")*(" + str(L) + "*12)^3/(3) = " + str(round(del_iD_L_EI,3)) + " in"
    # find required area of steel
    phif = 0.9
    design_math_1 += "\nφf = 0.9"
    if b <= h:
        j = 0.9
        design_math_1 += "\nj = 0.9"
    else:
        j = 0.95
        design_math_1 += "\nj = 0.95"
    if exposure == "No exposure to weather or ground":
        cover = 1.5
        design_math_1 += "\nCover = 1.5 in"
    elif exposure == "Exposed to weather or ground":
        cover = 2
        design_math_1 += "\nCover = 2 in"
    elif exposure == "Cast against and constant contact with ground":
        cover = 3
        design_math_1 += "\nCover = 3 in"
    d = h-cover-1
    design_math_1 += "\nd = h-cover-1     " + str(h) + "-" + str(cover) + "-1 = " + str(d) + " in"
    As_req = Mu*12/(phif*fy*j*d)
    design_math_1 += "\nAs_req = Mu*12/(φf*fy*j*d)     " + str(Mu) + "*12/" + str(phif) + "*" + str(fy) + "*" + str(j) + "*" + str(d) + " = " + str(round(As_req,3)) + " in^2"
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
    #printing all of initial desgin math
    print(design_math_1)
    #printing all math for Flexure check
    for i in range(len(flexure_rebar)):
        print(flexure_rebar_math[i])
    #quick flexure overview
    for i in range(len(flexure_rebar)):
        print("dc_ratio of " + str(num_of_bars[i]) + " #" + str(flexure_rebar[i]) + "bars: " + str(round(dc_ratio[i],3)))
    counter = 0
    for i in range(len(d)):
        if dc_ratio[i] < 0.05:
            counter +=1
    if counter == 4 and beam_type == "Singely Reinforced Unknown Dimensions":
        print("It appears something went wrong when making the beam, no size bars with any number of bars that can fit meet the  ACI318-19(22) code. Sorry for the inconvinence.")
        sys.exit()
    elif counter == 4:
        print("The given beam dimensions don't work for the loading.")
        sys.exit()
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
    design_math_2 = ""
    # How many bands/ Band strength
    phiv = 0.75
    design_math_2 += "\nΦv = 0.75"
    if wc <= 100:
        design_math_2 += "\nwc ≤ 100     " + str(wc) + " ≤ 100 Therefore λ = 0.75"
        lam = 0.75
    elif wc >= 135:
        design_math_2 += "\nwc ≥ 135     " + str(wc) + " ≤ 135 Therefore λ = 1"
        lam = 1
    else:
        lam = 0.0075*wc
        design_math_2 += "\n100 < wc < 135     100 < " + str(wc) + " < 135 Therefore λ = 0.0075*wc     0.0075*" + str(wc) + " = " + str(lam)
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
    if load == "point load" and beam_type == "Singely Reinforced Known Dimensions":
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
                V_of_beam[i] += W*(L/2-x_line[i])+P*x_line[i]/2
            elif B_type == "Cantilever":
                V_of_beam[i] += -W*x_line[i]-P*x_line[i]
        x_change = np.zeros((len(d_shear),3))
        for r in range(len(d_shear)):
            if B_type == "Simply Supported":
                x_counter = 0
                counter = 0
                while counter == 0:
                    if V_of_beam[x_counter] < phiv_Vc[r]:
                        x_change[r,0] = x_line[x_counter]
                        x_counter += 1
                        counter += 1
                    else:
                        x_counter += 1
                while counter == 1:
                    if V_of_beam[x_counter] < No_Stirrup[r]:
                        x_change[r,1] = x_line[x_counter]
                        x_counter += 1
                        counter += 1
                    else:
                        x_counter += 1
            elif B_type == "Cantilever":
                x_change[r,0] = -phiv_Vc[r]/(W+P)
                shear_math[r] += "\nL1 = -ϕvVc/(W+P)     -" + str(phiv_Vc) + "/(" + str(W) + "+" + str(P) + ") = " + str(x_change[r,0]) + " ft"
                x_change[r,1] = -No_Stirrup[r]/(W+P)
                shear_math[r] += "\nL1 = -No_stirrup/(W+P)     -" + str(No_Stirrup) + "/(" + str(W) + "+" + str(P) + ") = " + str(x_change[r,1]) + " ft"
            # bands being set up
        band_counter = np.ones(len(d_shear))
        for r in range(len(d_shear)):
            for col in range(3):
                if x_change[r,col] > 0:
                    band_counter[r] +=1     
        bands = int(max(band_counter))
        spacing = np.ones((len(d_shear),bands))
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
                        smax1 = d_shear[r]/2
                        shear_math[r] += "\nsmax1 = d/2     " + str(d_shear[r]) + "/2 = " + str(smax1) + " in"
                        smax2 = Av*fyt*1000/(0.75*fpc**0.5*b)
                        shear_math[r] += "\nsmax2 = Av*fyt*1000/(0.75*√(f'c)*b)     " + str(Av) + "*" + str(fyt) + "*1000/(0.75*√(" + str(fpc) + ")*" + str(b) + ") = " + str(round(smax2,3)) + " in"
                        smax3 = Av*fyt*1000/(50*b)
                        shear_math[r] += "\nsmax3 = Av*fyt*1000/(50*b)     " + str(Av) + "*" + str(fyt) + "*1000/(50*" + str(b) + ") = " + str(round(smax3,3)) + " in"
                        smax4 = 24
                        shear_math[r] += "\nsmax4 = 24 in"
                        spacing[r,cur_band] = int(min(smax1,smax2,smax3,smax4))
                        shear_math[r] += "\nsmax = " + str(spacing[r,cur_band])
                        cur_band += 1
            # finalizing spaces and lengths
            Ls_S = np.zeros((len(d_shear),bands))
            for r in range(len(d_shear)):
                if bands == 3:
                    Ls_S[r,0] = round(x_change[r,0]*12/spacing[r,0]+.5,0)*spacing[r,0]
                    shear_math[r] += "\nLength1 = next_whole_number(l1*12/s1)*s1     next_whole_number(l" + str(x_change[r,0]) + "*12/" + str(spacing[r,0]) + ")*" + str(spacing[r,0]) + " = " + str(Ls_S[r,0]) + " in"
                    Ls_S[r,1] = round(x_change[r,1]*12/spacing[r,1]+.5,0)*spacing[r,1]
                    shear_math[r] += "\nLength1 = next_whole_number(l2*12/s2)*s2     next_whole_number(l" + str(x_change[r,1]) + "*12/" + str(spacing[r,1]) + ")*" + str(spacing[r,1]) + " = " + str(Ls_S[r,1]) + " in"
                    Ls_S[r,2] = 0
                elif bands == 2:
                    Ls_S[r,0] = round(x_change[r,1]*12/spacing[r,0]+.5,0)*spacing[r,0]
                    shear_math[r] += "\nLength1 = next_whole_number(l1*12/s1)*s1     next_whole_number(l" + str(x_change[r,0]) + "*12/" + str(spacing[r,0]) + ")*" + str(spacing[r,0]) + " = " + str(Ls_S[r,0]) + " in"
                    Ls_S[r,1] = 0
            # checking spacing across the beam for distributed loads
            Note = [""]*len(d_shear)
            if bands == 3:
                s_len = np.zeros(len(d_shear))
                s_len_act = np.zeros(len(d_shear))
                counter = 0
                for i in range(len(d_shear)):
                    s1 = d_shear[i]/2
                    shear_math[i] += "\ns1 = d/2     " + str(d_shear[i]) + "/2 = " + str(s1) + " in"
                    s2 = 12
                    shear_math[i] += "/ns2 = 12 in"
                    s_len[i] = min(s1,s2)
                    shear_math[i] += "/ns = " + str(s_len[i]) + " in"
                    s_len_act[i] = (b-2*cover)/(Legs-1)
                    shear_math[i] += "s_act = (b-2*cover)/(Legs-1)     (" + str(b) + "-2*" + str(cover) + ")/(" + str(Legs) + "-1) = " + str(s_len_act[i]) + " in"
                    if s_len[i] < s_len_act[i]:
                        shear_math[i] += "s < s_act     " + str(s_len[i]) + " < " + str(s_len_act[i]) + " THE BEAM HAS FAILED DO NOT USE!"
                        Note[i] += "\nTHIS BEAM FAILS LEG SPACING AND ISN'T UP TO CODE!"
                    else:
                        counter +=1
                        shear_math[i] += "s ≥ s_act     " + str(s_len[i]) + " ≥ " + str(s_len_act[i])
                if counter == 0:
                    print("The number of leggs don't meet the minimum required spacing, please try with more legs.")
                    sys.exit()
            elif bands == 2:
                s_len = np.zeros(len(d_shear))
                s_len_act = np.zeros(len(d_shear))
                counter = 0
                for i in range(len(d_shear)):
                    s1 = d_shear[i]/2
                    shear_math[i] += "\ns1 = d     " + str(d_shear[i]) + " = " + str(s1) + " in"
                    s2 = 24
                    shear_math[i] += "/ns2 = 24 in"
                    s_len[i] = min(s1,s2)
                    shear_math[i] += "/ns = " + str(s_len[i]) + " in"
                    s_len_act[i] = (b-2*cover)/(Legs-1)
                    shear_math[i] += "s_act = (b-2*cover)/(Legs-1)     (" + str(b) + "-2*" + str(cover) + ")/(" + str(Legs) + "-1) = " + str(s_len_act[i]) + " in"
                    if s_len[i] < s_len_act[i]:
                        shear_math[i] += "s < s_act     " + str(s_len[i]) + " < " + str(s_len_act[i]) + " THE BEAM HAS FAILED DO NOT USE!"
                        Note[i] += "\nTHIS BEAM FAILS LEG SPACING AND ISN'T UP TO CODE!"
                    else:
                        counter +=1
                        shear_math[i] += "s ≥ s_act     " + str(s_len[i]) + " ≥ " + str(s_len_act[i])
                if counter == 0:
                    print("The number of leggs don't meet the minimum required spacing, please try with more legs.")
                    sys.exit()
            # checking shear if past 2 bands since will then need to check if max shear is resisted by shear bands
            if bands == 3:
                phi_Vs_max = np.zeros(len(d_shear))
                phi_V_max = np.zeros(len(d_shear))
                counter = 0
                for i in range(len(d_shear)):
                    phi_Vs_max[i] = 0.9*Av*fyt*d_shear[i]/spacing[i,0]
                    shear_math[i] += "ϕVs = ϕ_v*Av*fyt*d/s     0.9" + str(Av) + "*" + str(fyt) + "*" + str(d_shear[i]) + "/" + str(spacing[i,0]) + " = " + str(phi_Vs_max[i]) + " k"
                    phi_V_max[i] += phi_Vs_max[i] + phiv_Vc[i]
                    shear_math[i] += "ϕV = ϕVc+ϕVs     " + str(phiv_Vc[i]) + "+" + str(phiv_Vc[i]) + " = " + str(phi_V_max[i])
                    if d_away == True:
                        location = round(d_shear[i]-0.5)
                        Vu = V_of_beam[0]
                    else:
                        Vu = V_of_beam[0]
                    if phi_V_max[i] < Vu:
                        shear_math[i] += "ϕV < Vu     " + str(phi_V_max[i]) + " < " + str(Vu + " THE BEAM HAS FAILED DO NOT USE!")
                        Note[i] += "\nTHIS BEAM FAILS IN SHEAR AND ISN'T UP TO CODE!"
                    else:
                        counter +=1
                        shear_math[i] += "ϕV ≥ Vu     " + str(phi_V_max[i]) + " ≥ " + str(Vu)
                if counter == 0:
                    print("The beam cant handle the max shear add more shear strength or concrete strength.")
                    sys.exit()
            #printing all math for Shear design
            for i in range(len(d_shear)):
                print(shear_math[i])
            #quick shear overview
            print("Shear Overview for #" + str(Stirrup_size) + " with " + str(Legs) + " legs.")
            for i in range(len(d_shear)):
                if bands == 3:
                    print(str(working_bar[i]) + ": Band1 = Stops at " + str(Ls_S[i,0]) + " in spaced at " + str(spacing[i,0]) + " in.")
                    print("     Band2 = Stops at " + str(Ls_S[i,1]) + " in spaced at " + str(spacing[i,1]) + " in.")
                    if B_type == "Simply Supported":
                        print("     No stirrups required for remaining half of beam and the two halfs are mirrors of eachother.")
                    elif B_type == "Cantilever":
                        print("     No stirrups required for the rest of the beam")
                elif bands == 2:
                    print(str(working_bar[i]) + ": Band1 = Stops at " + str(Ls_S[i,0]) + " in spaced at " + str(spacing[i,0]) + " in.")
                    if B_type == "Simply Supported":
                        print("     No stirrups required for remaining half of beam and the two halfs are mirrors of eachother.")
                    elif B_type == "Cantilever":
                        print("     No stirrups required for the rest of the beam")
                elif load == "point load":
                    print(str(working_bar[i]) + ": Only 1 Band spaced at " + str(smax[i]) + " in.")
    #deflection solving
    deflection_math = [""]*len(d_shear)
    # set values since not designing doubly reinforced
    rebar_shape = "Singly Reinforced"
    Asp = 0
    del_long = np.zeros(len(d_shear))
    for i in range(len(d_shear)):
        deflection_math[i] += "\nDeflection for beam with " + str(num_of_bars[i]) + " #" + str(flexure_rebar[i]) + "bars: "
        if B_type == "Simply Supported":
            h_min = L*12/16
            deflection_math[i] += "\nh_min = L*12/16     " + str(L) + "*12/16 = " + str(h_min) + " in"
        elif B_type == "Cantilever":
            h_min = L*12/8
            deflection_math[i] += "\nh_min = L*12/8     " + str(L) + "*12/8 = " + str(h_min) + " in"
        if h_min <= h and Non_Struct == "False":
            deflection_math[i] += "\nh_min ≤ h     " + str(h_min) + " ≤ " + str(h) + " and No structural Elements are attached meaning no need to check deflection."
            sys.exit()
        # moments of inertia calcs
        Ig = 1/12*b*h**3
        deflection_math[i] += "\nIg = 1/12*b*h^3     1/12*" + str(b) + "*" + str(h) + "^3 = " + str(Ig) + " in^4"
        Ec = wc**1.5*33*fpc**0.5/1000
        deflection_math[i] += "\nEc = w^1.5*33*√(f'c)/1000     " + str(wc) + "^1.5*33*√(" + str(fpc) + ")/1000 = " + str(round(Ec,3)) + " ksi"
        n = 29000/Ec
        deflection_math[i] += "\nn = Es/Ec     29000/" + str(round(Ec,3)) + " = " + str(round(n,3))
        if rebar_shape == "Singly Reinforced":
            quad_a = b/2
            deflection_math[i] += "\na = b/2     " + str(b) + "/2 = " + str(quad_a)
            quad_b = n*As[i]
            deflection_math[i] += "\nb = n*As     " + str(round(n,3)) + "*" + str(As) + " = " + str(round(quad_b))
            quad_c = -n*As[i]*d_shear[i]
            deflection_math[i] += "\nc = -n*As*d     -" + str(round(n,3)) + "*" + str(As) + "*" + str(d_shear[i]) + " = " + str(round(quad_c))
            c1 = (-quad_b+(quad_b**2-4*quad_a*quad_c)**0.5)/(2*quad_a)
            c2 = (-quad_b-(quad_b**2-4*quad_a*quad_c)**0.5)/(2*quad_a)
            deflection_math[i] += "\nc = (-b±√(b^2-4ac)/(2a)     (-" + str(round(quad_b,3)) + "±√(" + str(round(quad_b,3)) + "^2-4*" + str(round(quad_a,3)) + "*" + str(round(quad_c,3)) + ")/(2*" + str(round(quad_a,3)) + ") = " + str(round(c1,3)) + ", " + str(round(c2,3))
            if c1 < 0 and c2 < 0:
                print("An error occured and both values of c where negative which cant happen, sorry for the inconvienence.")
                sys.exit()
            elif c1 < 0:
                c = c2
                deflection_math[i] += "\nUse c = " + str(round(c2,3)) + " in"
            elif c2 < 0:
                c = c1
                deflection_math[i] += "\nUse c = " + str(round(c1,3)) + " in"
            elif c1 < c2:
                c = c1
                deflection_math[i] += "\nUse c = " + str(round(c1,3)) + " in"
            elif c2 < c1:
                c = c2
                deflection_math[i] += "\nUse c = " + str(round(c2,3)) + " in"
            else:
                print("Something went wrong when calculating c sorry for the inconvienence.")
                sys.exit()
            Icr = 1/3*b*c**3+n*As[i]*(c-d_shear[i])**2
            deflection_math[i] += "\nIcr = 1/3*b*c^3+n*As*(c-d)^2     1/3*" + str(b) + "*" + str(round(c)) + "^3+" + str(round(n)) + "*" + str(As) + "*(" + str(round(c)) + "-" + str(d_shear[i]) + "^2 = " + str(round(Icr,3)) + " in^4"
        #Mcr Calc
        if wc <= 100:
            deflection_math[i] += "\nwc ≤ 100     " + str(wc) + " ≤ 100 Therefore λ = 0.75"
            lam = 0.75
        elif wc >= 135:
            deflection_math[i] += "\nwc ≥ 135     " + str(wc) + " ≤ 135 Therefore λ = 1"
            lam = 1
        else:
            lam = 0.0075*wc
            deflection_math[i] += "\n100 < wc < 135     100 < " + str(wc) + " < 135 Therefore λ = 0.0075*wc     0.0075*" + str(wc) + " = " + str(lam)
        fr = 7.5*lam*fpc**0.5
        deflection_math[i] += "\n7.5*λ*√(f'c)     7.5*" + str(lam) + "*√(" + str(fpc) + " = " + str(round(fr,3)) + " psi"
        yt = h/2
        deflection_math[i] += "\nyt = h/2     " + str(h) + "/2 = " + str(yt) + " in"
        Mcr = fr*Ig/yt/(1000*12)
        deflection_math[i] += "\nMcr = fr*Ig/yt/(1000*12)     " + str(fr) + "*" + str(round(Ig,3)) + "/" + str(yt) + "/(1000*12) = " + str(round(Mcr,3)) + " kft"
        # moment calcs
        if B_type == "Simply Supported" :
            if load == "point load" and beam_type == "Singely Reinforced Known Dimensions":
                deflection_math[i] += "\nM = P*L/4"
                M_dl = P_d*L/4
                deflection_math[i] += "\nM_dl = " + str(P_d) + "*" + str(L) + "/4 = " + str(M_dl) + " kft"
                M_dl_ll = (P_d+P_l)*L/4
                deflection_math[i] += "\nM_dl_ll = (" + str(P_d) + "+" + str(P_l) + ")*" + str(L) + "/4 = " + str(M_dl) + " kft"
            elif load == "distributed load":
                deflection_math[i] += "\nM = w*L^2/8"
                M_dl = w_d*L**2/8
                deflection_math[i] += "\nM_dl = " + str(w_d) + "*" + str(L) + "^2/8 = " + str(M_dl) + " kft"
                M_dl_ll = (w_d+w_l)*L**2/8
                deflection_math[i] += "\nM_dl_ll = (" + str(w_d) + "+" + str(w_l) + ")*" + str(L) + "^2/8 = " + str(M_dl) + " kft"
            elif load == "point load" and beam_type == "Singely Reinforced Unknown Dimensions":
                M_dl = w_d*L**2/8+P_d*L/4
                deflection_math[i] += "\nM_dl = w_d*L^2/8+P_d*L/4     " + str(w_d) + "*" + str(L) + "^2/8+" + str(P_d) + "*" + str(L) + "/4 = " + str(M_dl) + " kft"
                M_dl_ll = W2*L**2/8+P2*L/4
                deflection_math[i] += "\nM_dl_ll = (w_d+w_l)*L^2/8+(P_d+P_l)*L/4     (" + str(w_d) + "+" + str(w_l) + ")*" + str(L) + "^2/8+(" + str(P_d) + "+" + str(P_l) + ")*" + str(L) + "/4 = " + str(M_dl_ll) + " kft"
        elif B_type == "Cantilever":
            if load == "point load" and beam_type == "Singely Reinforced Known Dimensions":
                deflection_math[i] += "\nM = P*L"
                M_dl = P_d*L
                deflection_math[i] += "\nM_dl = " + str(P_d) + "*" + str(L) + " = " + str(M_dl) + " kft"
                M_dl_ll = (P_d+P_l)*L
                deflection_math[i] += "\nM_dl_ll = (" + str(P_d) + "+" + str(P_l) + ")*" + str(L) + " = " + str(M_dl) + " kft"
            elif load == "distributed load":
                deflection_math[i] += "\nM = w*L^2/2"
                M_dl = w_d*L**2/2
                deflection_math[i] += "\nM_dl = " + str(w_d) + "*" + str(L) + "^2/2 = " + str(M_dl) + " kft"
                M_dl_ll = (w_d+w_l)*L**2/2
                deflection_math[i] += "\nM_dl_ll = (" + str(w_d) + "+" + str(w_l) + ")*" + str(L) + "^2/2 = " + str(M_dl) + " kft"
            elif load == "point load" and beam_type == "Singely Reinforced Unknown Dimensions":
                M_dl = w_d*L**2/2+P_d*L
                deflection_math[i] += "\nM_dl = w_d*L^2/2+P_d*L     " + str(w_d) + "*" + str(L) + "^2/2+" + str(P_d) + "*" + str(L) + " = " + str(M_dl) + " kft"
                M_dl_ll = (w_d+w_l)*L**2/2+(P_d+P_l)*L
                deflection_math[i] += "\nM_dl_ll = (w_d+w_l)*L^2/8+(P_d+P_l)*L/4     (" + str(w_d) + "+" + str(w_l) + ")*" + str(L) + "^2/2+(" + str(P_d) + "+" + str(P_l) + ")*" + str(L) + " = " + str(M_dl_ll) + " kft"
        #calcing Ie
        if M_dl <= 2/3*Mcr:
            deflection_math[i] += "\nM_dl <= 2/3*Mcr     " + str(M_dl) + " ≤ 2/3*" + str(round(Mcr,3)) + " = " + str(round(2/3*Mcr))
            Ie_dl = Ig
            deflection_math[i] += "\nTherefore Ie_dl = Ig     Ie_dl = " + str(round(Ig,3)) + " in^4"
        else:
            deflection_math[i] += "\nM_dl > 2/3*Mcr     " + str(M_dl) + " > 2/3*" + str(round(Mcr,3)) + " = " + str(round(2/3*Mcr)) + " Need to calc Ie_dl"
            Ie_dl = Icr/(1-(2/3*Mcr/M_dl)**2*(1-Icr/Ig))
            deflection_math[i] += "\nIe_dl = Icr/(1-(2/3*Mcr/M_dl)^2*(1-Icr/Ig))     " + str(round(Icr,3)) + "/(1-(2/3*" + str(round(Mcr,3)) + "/" + str(round(M_dl,3)) + ")^2*(1-" + str(round(Icr,3)) + "/" + str(round(Ig,3)) + " = " + str(Ie_dl) + " in^4"
        if M_dl_ll <= 2/3*Mcr:
            deflection_math[i] += "\nM_dl_ll ≤ 2/3*Mcr     " + str(M_dl_ll) + " ≤ 2/3*" + str(round(Mcr,3)) + " = " + str(round(2/3*Mcr))
            Ie_dl_ll = Ig
            deflection_math[i] += "\nTherefore Ie_dl_ll = Ig     Ie_dl_ll = " + str(round(Ig,3)) + " in^4"
        else:
            deflection_math[i] += "\nM_dl_ll > 2/3*Mcr     " + str(M_dl_ll) + " > 2/3*" + str(round(Mcr,3)) + " = " + str(round(2/3*Mcr)) + " Need to calc Ie_dl"
            Ie_dl_ll = Icr/(1-(2/3*Mcr/M_dl_ll)**2*(1-Icr/Ig))
            deflection_math[i] += "\nIe_dl = Icr/(1-(2/3*Mcr/M_dl_ll)^2*(1-Icr/Ig))     " + str(round(Icr,3)) + "/(1-(2/3*" + str(round(Mcr,3)) + "/" + str(round(M_dl_ll,3)) + ")^2*(1-" + str(round(Icr,3)) + "/" + str(round(Ig,3)) + " = " + str(Ie_dl_ll) + " in^4"
        # calcing deflections
        del_iD = del_iD_EI/(Ec*Ie_dl)
        deflection_math[i] += "\nΔ_iD = Δ_iD*Ec*Ie_dl/(Ec*Ie_dl)     " + str(del_iD_EI) + "/(" + str(Ec) + "*" + str(Ie_dl) + ") = " + str(del_iD) + " in"
        del_iD_L = del_iD_L_EI/(Ec*Ie_dl_ll)
        deflection_math[i] += "\nΔ_iD_L = Δ_iD_L*Ec*Ie_dl_L/(Ec*Ie_dl_L)     " + str(del_iD_L_EI) + "/(" + str(Ec) + "*" + str(Ie_dl_ll) + ") = " + str(del_iD_L) + " in"
        del_iL = del_iD_L-del_iD
        deflection_math[i] += "\nΔ_iL = Δ_iD_L-Δ_iD     " + str(round(del_iD_L,3)) + "-" + str(round(del_iD,3)) + " = " + str(round(del_iL,3))
        #allowable deflection
    counter1 = 0
    counter2 = 0
    for i in range(len(d_shear)):
        # might need to create a question for if floor or flat roof since diffrent
        del_short_allowed = L*12/360
        counter = 0
        deflection_math[i] += "\nΔ_short_allowed = L*12/360     " + str(L) + "*12/360 = " + str(round(del_short_allowed,3)) + " in"
        if del_iL > del_short_allowed:
            deflection_math[i] += "\nΔ_iL > Δ_short_allowed     " + str(round(del_iL,3)) + " > " + str(round(del_short_allowed,3)) + " Therefore it isn't to code and doesn't work"
            Note[i] += "\nTHIS BEAM FAILED IN SHORT TERM DEFLECTION AND ISN'T UP TO CODE!"
        else:
            deflection_math[i] += "\nΔ_iL ≤ Δ_short_allowed     " + str(round(del_iL,3)) + " ≤ " + str(round(del_short_allowed,3)) + " Good"
            counter1 += 1
        del_iLs = percent/100*del_iL
        deflection_math[i] += "\nΔ_iLs = " + str(percent) + "/100*" + str(del_iL) + " = " + str(round(del_iLs,3)) + " in"
        lam_infinite = 2/(1+50*Asp/(b*d_shear[i]))
        deflection_math[i] += "\nλ_∞ = 2/(1+50*As'/(b*d))     2/(1+50*" + str(Asp) + "/(" + str(b) + "*" + str(d_shear[i]) + ")) = " + str(round(lam_infinite))
        lam_t_0 = zata_s/(1+50*Asp/(b*d_shear[i]))
        deflection_math[i] += "\nλ_t_0 = ζ/(1+50*As'/(b*d))     " + str(zata_s) + "/(1+50*" + str(Asp) + "/(" + str(b) + "*" + str(d_shear[i]) + ")) = " + str(round(lam_t_0))
        lam_t_0_infinite = lam_infinite-lam_t_0
        deflection_math[i] += "\nλ_t_0_∞ = λ_∞-λ_t_0     " + str(lam_infinite) + "-" + str(lam_t_0) + " = " + str(lam_t_0_infinite)
        del_long[i] = lam_t_0_infinite*del_iD+del_iL+lam_infinite*del_iLs
        deflection_math[i] += "\nΔ_long = λ_t_0_∞*Δ_iD+Δ_iL+λ_∞*Δ_iLs     " + str(lam_t_0_infinite) + "*" + str(round(del_iD,3)) + "+" + str(round(del_iL,3)) + "+" + str(lam_infinite) + "*" + str(round(del_iLs,3)) + " = " + str(round(del_long[i],3)) + " in"
        del_long_allowed = L*12/480
        deflection_math[i] += "\nΔ_long_allowed = L*12/480     " + str(L) + "*12/480 = " + str(round(del_long_allowed,3)) + " in"
        counter = 0
        if del_long[i] > del_long_allowed:
            deflection_math[i] += "\nΔ_long > Δ_long_allowed     " + str(round(del_long[i],3)) + " > " + str(round(del_long_allowed,3)) + " Therefore it isn't to code and doesn't work"
            Note[i] += "\nTHIS BEAM FAILED IN SHORT TERM DEFLECTION AND ISN'T UP TO CODE!"
        else:
            deflection_math[i] += "\nΔ_long ≤ Δ_long_allowed     " + str(round(del_long[i],3)) + " ≤ " + str(round(del_long_allowed,3)) + " Good the beam works"
            counter2 += 1
    if counter1 == 0:
        print("THE BEAM FAILED IN SHORT TERM DEFLECTION!")
        sys.exit()
    if counter2 == 0:
        print("THE BEAM FAILED IN LONG TERM DEFLECTION!")
        sys.exit()
    #print all of deflection calcs
    for i in range(len(d_shear)):
        print(deflection_math[i])
        
    # Deflection over view
    print("Deflection Overview")
    for i in range(len(d_shear)):
        print("A displacement of " + str(round(del_long[i],3)) + " in occured in the beam with " + str(working_bar_number[i]) + " #" + str(working_bar[i]) + "bars" )

    #All info printed in one for flexure shear and deflection
    print()
    print()
    print("Overview for Beams Designed")
    if beam_type == "Singely Reinforced Unknown Dimensions":
        print("The beam dimensions are, b: " + str(b) + " in")
        print("                         h: " + str(h) + " in")
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
        print(Note[i])
        print()
    # Which of the beams do you want the math for
    Choices = [""]*(len(d_shear))
    for i in range(len(d_shear)):
        Choices[i] = "Beam with " + str(working_bar_number[i]) + " #" + str(working_bar[i]) + "bars."
    question = "What beam would you like the print out for"
    options = Choices
    if __name__ == "__main__":
        chosen = choice(question, options)
    for i in range(len(d_shear)):
        if chosen == Choices[i]:
            output = i
    print()
    print()
    print(design_math_1[output])
    print(flexure_rebar_math[output])
    print(design_math_2[output])
    print(deflection_math[output])