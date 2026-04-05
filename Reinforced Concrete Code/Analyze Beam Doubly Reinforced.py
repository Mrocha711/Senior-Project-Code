# -*- coding: utf-8 -*-
"""
Created on Sat Apr  4 10:53:46 2026

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
