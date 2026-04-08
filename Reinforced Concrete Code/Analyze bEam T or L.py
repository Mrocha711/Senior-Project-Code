# -*- coding: utf-8 -*-
"""
Created on Sat Apr  4 10:55:41 2026

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