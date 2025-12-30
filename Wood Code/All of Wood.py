# -*- coding: utf-8 -*-
"""
Created on Wed Nov 19 15:41:54 2025

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
from PyQt5.QtWidgets import (QApplication, QDialog, QVBoxLayout, QLabel, QLineEdit, QComboBox, QPushButton, QHBoxLayout, QMessageBox)
# imports end --------------------------------------------------------------------------------

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

class MultiInputDialog(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Test")
        self.setGeometry(1, 30, 1060, 960)
        
        layout = QVBoxLayout()
        self.inputs = []
        
        for question in questions:
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
            QMessageBox.warning(
                self, "Invalid Input",
                "Please enter valid numeric values (e.g. 3.14, -2.5)."
            )

    def cancel(self):
        self.reject()  # Closes dialog and marks it as canceled


def get_inputs():
    dialog = MultiInputDialog()
    if dialog.exec_() == QDialog.Accepted:
        return dialog.results  # Return all answers as a list
    else:
        sys.exit()

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

questions = "What are we solving."
options = ['Analysis', 'Desgin']
if __name__ == '__main__':
    Problem = choice(questions, options)
    
if Problem == "Analysis":
    questions = "What values are we solving."
    options = ['Adjusted Values','Beam', 'Column']
    if __name__ == '__main__':
        Solve_Values = choice(questions, options)
    
    #creating array of sizes to ask what size
    df = pd.read_excel('Wood_tables.xlsx', sheet_name='Size Properties ', engine='openpyxl')
    sizes = df.iloc[:, 0].astype(str)
    
    if Solve_Values == "Adjusted Values":
        questions = ["What size"]
        options = [sizes.tolist()]
        if __name__ == '__main__':
            size = MultiDrop(questions, options)
            size = str(size[0])
        
        #Grabbing all size info
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
            print("An error occured.")
            sys.exit()
    
        #creating array of all speices
        Speices_list = my_class + " Ref Values Speices"
        df = pd.read_excel('Wood_tables.xlsx', sheet_name= Speices_list, engine='openpyxl') 
        Speices = df.iloc[:, 0].astype(str)
    
        questions = ["What speices"]
        options = [Speices.tolist()]
        if __name__ == '__main__':
            speices = MultiDrop(questions, options)
            speices = speices[0]
    
        #getting all other required values
        Ref_values = my_class + " Ref Values"
        df = pd.read_excel('Wood_tables.xlsx', sheet_name= Ref_values, engine='openpyxl') 
        match = df[df["Species"] == speices]
        if not match.empty:
            Grades = match.iloc[:,1].astype(str)
        else:
            print("An error occured.")
            sys.exit()
        
        Desgin_load = ["permanent", "live", "snow", "construction", "wind/eq", "impact"]
        True_False = ["False", "True"]
        Temp_range = ["T<100F", "100F<T<125F", "T>125F"]
        Supports = ["cantilever", "simply supported"]
        
        questions = ["What grade", "What load type", "Moisture present", "Temprature range", "Is it in flat use", "Is it insicesed", "Is it repetitive", "Support type", "Laterally resisted", "Is it Braced"]
        options = [Grades, Desgin_load, True_False, Temp_range, True_False, True_False, True_False, Supports, True_False, True_False]
        if __name__ == '__main__':
            grade, load_dur, Mouister, Temprature, flat, incised, repetitive, Support, Lateral, braced = MultiDrop(questions, options)
        
        #What loading configuration
        if Support == "cantilever":
            load_config = ["uniformly distributed", "concentrated load at center", "other"]
            questions = ["What is the loading"]
            options = [load_config]
            if __name__ == '__main__':
                load = MultiDrop(questions, options)
        else:
            load_config = ["uniformly distributed", "concentrated load at center", "2 concentrated loads evenly spaced with supports", "3 concentrated loads evenly spaced with supports", "4 concentrated loads evenly spaced with supports", "5 concentrated loads evenly spaced with supports", "6 concentrated loads evenly spaced with supports", "7 concentrated loads evenly spaced with supports", "equal end moments", "other"]
            questions = ["What is the loading"]
            options = [load_config]
            if __name__ == '__main__':
                load = MultiDrop(questions, options)
        load = load[0]
        
        #required numbers
        questions = ["length of members longest unsupported distance in ft", "length of bearing in in"]
        if __name__ == '__main__':
            length, lb = get_inputs()
        
        # table of values
        Values = np.ones((7,12))
        # If anything needs to be noted
        Note = ""
        
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
                        final_match = final_match[match['Grade'] == grade]
                        if not final_match.empty:
                            final_match_np = final_match.to_numpy()
                            Values[0,0] = final_match_np[0, 3]
                            Values[1,0] = final_match_np[0, 4]
                            Values[2,0] = final_match_np[0, 5]
                            Values[3,0] = final_match_np[0, 6]
                            Values[4,0] = final_match_np[0, 7]
                            Values[5,0] = final_match_np[0, 8]
                            Values[6,0] = final_match_np[0, 9]
        
        #getting Cd
        df = pd.read_excel('Wood_tables.xlsx', sheet_name='CD', engine='openpyxl') 
        match = df[df["Load Duration"] == load_dur]
        if not match.empty:
            match_np = match.to_numpy() # ChatGpt assisted
            Values[0,1] = match_np[0, 1]
            Values[1,1] = match_np[0, 1]
            Values[2,1] = match_np[0, 1]
            Values[4,1] = match_np[0, 1]
        
        # getting CM
        if Mouister == "True":
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
        if Temprature == "T>125F":
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
        elif Temprature == "100F<T<125F":
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
            CF_math =""
            test_1 = Values[0,0]*Values[0,5]
            CF_math += "Fb*CF     " + str(Values[0,0]) + "*" + str(Values[0,5]) + " = " + str(test_1)
            if test_1 <= 1150:
                CF_math += "\nFb*CF ≤ 1150    " + str(test_1) + "≤ 1150 there for CF = 1"
                Values[0,2] = 1
            else:
                CF_math += "\nFb*CF ≥ 1150    " + str(test_1) + "≥ 1150 there for CF = 0.85"
            test_2 = Values[4,0]*Values[4,5]
            CF_math += "\nFc*CF     " + str(Values[4,0]) + "*" + str(Values[0,5]) + " = " + str(test_2)
            if test_2 <= 750:
                CF_math += "\nFc*CF ≤ 750    " + str(test_2) + "≤ 750 there for CF = 1"
                Values[4,2] = 1
            else:
                CF_math += "\nFc*CF ≥ 750    " + str(test_2) + "≥ 750 there for CF = 0.8"

        # getting CFu
        if flat == "True":
            if d_act == b_act:
                Values[0,6] = 1
                Values[1,6] = 1
                Values[4,6] = 1
            else:
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
                            print("Something went wrong, the size given was detected to be small but had no CFu rule applied so program terminated.")
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
        if incised == "True":
            Values[0,7] = 0.8
            Values[1,7] = 0.8
            Values[2,7] = 0.8
            Values[4,7] = 0.8
            Values[5,7] = 0.95
            Values[6,7] = 0.95
            
        # getting Cr
        if repetitive == "True":
            Values[0,8] = 1.15

        #getting CL
        CL_math = ""
        if d_nom <= b_nom:
            CL_math += "d≤b     " + str(d_nom) + "≤" + str(b_nom) + "    therefore CL = 1"
            Values[0,4] = 1
        elif Lateral == "True":
            CL_math += "It is laterally braced"
            Values[0,4] = 1
        else:
            CL_math += "d>b     " + str(d_nom) + ">" + str(b_nom)
            lu = length*12/d_act
            CL_math += "\nlu/d     " + str(length) + "/" + str(d_act) + " = " + str(lu)
            if Support == "cantilever":
                if load == "uniformly distributed":
                    if lu < 7:
                        le = 1.33*length*12
                        CL_math += "\nle=1.33lu*12     1.33*" + str(length) + "*12 = " + str(le)
                    else:
                        le = 0.9*length*12+3*d_act
                        CL_math += "\nle=0.9lu*12+3d     0.9*" + str(length) + "*12+3*" + str(d_act) + " = " + str(le)
                elif  load == "concentrated load at end":
                    if lu < 7:
                        le = 1.87*length*12
                        CL_math += "\nle=1.87lu*12     1.87*" + str(length) + "*12 = " + str(le)
                    else:
                        le = 1.44*length*12+3*d_act
                        CL_math += "\nle=1.44lu+3d     1.44*" + str(length) + "*12+3*" + str(d_act) + " = " + str(le)
            elif Support == "simply supported":
                if load == "uniformly distributed":
                    if lu < 7:
                        le = 2.06*length*12
                        CL_math += "\nle=2.06lu*12     2.06*" + str(length) + "*12 = " + str(le)
                    else:
                        le = 1.63*length*12+3*d_act
                        CL_math += "\nle=1.63lu*12+3d     1.63*" + str(length) + "*12+3*" + str(d_act) + " = " + str(le)
                elif load == "concentrated load at center":
                    if lu < 7:
                        le = 1.8*length*12
                        CL_math += "\nle=1.8lu*12     1.8*" + str(length) + "*12 = " + str(le)
                    else:
                        le = 1.37*length*12+3*d_act
                        CL_math += "\nle=1.37lu*12+3d     1.37*" + str(length) + "*12+3*" + str(d_act) + " = " + str(le)
                elif load == "2 concentrated loads even with support":
                    le = 1.11*length*12
                    CL_math += "\nle=1.11lu*12     1.11*" + str(length) + "*12 = " + str(le)
                elif load == "3 concentrated loads even with support":
                    le = 1.68*length*12
                    CL_math += "\nle=1.68lu*12     1.68*" + str(length) + "*12 = " + str(le)
                elif load == "4 concentrated loads even with support":
                    le = 1.54*length*12
                    CL_math += "\nle=1.54lu*12     1.54*" + str(length) + "*12 = " + str(le)
                elif load == "5 concentrated loads even with support":
                    le = 1.68*length*12
                    CL_math += "\nle=1.68lu*12     1.68*" + str(length) + "*12 = " + str(le)
                elif load == "6 concentrated loads even with support":
                    le = 1.73*length*12
                    CL_math += "\nle=1.73lu*12     1.73*" + str(length) + "*12 = " + str(le)
                elif load == "7 concentrated loads even with support":
                    le = 1.84*length*12
                    CL_math += "\nle=1.84lu*12     1.84*" + str(length) + "*12 = " + str(le)
                elif load == "equal end moments":
                    le = 1.84*length*12
                    CL_math += "\nle=1.84lu*12     1.84*" + str(length) + "*12 = " + str(le)
                elif load == "Other":
                    if lu < 7:
                        le = 2.06*length*12
                        CL_math += "\nle=2.06lu*12     2.06*" + str(length) + "*12 = " + str(le)
                    elif lu <= 14.3:
                        le = 1.63*length*12+3*d_act
                        CL_math += "\nle=1.63lu*12+3d     1.63*" + str(length) + "*12+3*" + str(d_act) + " = " + str(le)
                    else:
                        le = 1.84*length*12
                        CL_math += "\nle=1.84lu*12     1.84*" + str(length) + "*12 = " + str(le)
                else:
                    print("The load you asgined for the simply supported was not from the ten options, double check you chose properly and typed it properly.")
                    sys.exit()
            else:
                print("The support you asgined was not from the two options, double check you chose properly and typed it properly.")
                sys.exit()
            Rb = ((le*d_act)/b_act**2)**(1/2)
            CL_math += "\nRb = √((le*d)/b**2)     √((" + str(le) + "*" + str(d_act) + ")/" + str(b_act) + "^2) = " + str(round(Rb,3))
            Emin_prime = math.prod(Values[6])
            CL_math += "\nE_min' = " + str(Values[6,0]) + "*" + str(Values[6,1]) + "*" + str(Values[6,2]) + "*" + str(Values[6,3]) + "*" + str(Values[6,4]) + "*" + str(Values[6,5]) + "*" + str(Values[6,6]) + "*" + str(Values[6,7]) + "*" + str(Values[6,8]) + "*" + str(Values[6,9]) + "*" + str(Values[6,10]) + "*" + str(Values[6,11]) + " = " + str(Emin_prime) + " psi"
            FbE = 1.2*Emin_prime/Rb**2
            CL_math += "\nFbE = 1.2Emin/Rb^2     1.2*" + str(Values[6,0]) + "/" + str(round(Rb,3)) + "^2 = " + str(round(FbE,3))
            Fbs = math.prod(Values[0])/Values[0,6]
            CL_math += "\nFb*=" + str(Values[0,0]) + "*" + str(Values[0,1]) + "*" + str(Values[0,2]) + "*" + str(Values[0,3]) + "*" + str(Values[0,5]) + "*" + str(Values[0,7]) + "*" + str(Values[0,8]) + " = " + str(Fbs)
            F = FbE/Fbs
            CL_math += "\nF = FbE/Fb*     " + str(round(FbE,3)) + "/" + str(Fbs) + " = " + str(round(F,3))
            Cl = (1+F)/1.9-(((1+F)/1.9)**2-F/0.95)**(1/2)
            CL_math += "\n(1+F)/1.9-√(((1+F)/1.9)^2-F/0.95)     (1+" + str(round(F,3)) + ")/1.9-√(((1+" + str(round(F,3)) + ")/1.9)^2-" + str(round(F,3)) + "/0.95) = " + str(round(Cl,3))
            Values[0,4] = Cl

        #getting Cp
        Cp_math = ""
        if Lateral == "True":
            Values[4,9] = 1
            Cp_math += "Cp = 1 since laterally supported"
        else:
            Cp_math += "Assuming Ke=1"
            le1 = length*12/d_act
            le2 = length*12/b_act
            le = max(le1,le2)
            if le > 50:
                Note += "Warning Column length effective is larger than allowed."
            Cp_math += "\nle1 = length/d     " + str(length) + "*12/" + str(d_act) + " = " + str(round(le1,3))
            Cp_math += "\nle2 = length/b     " + str(length) + "*12/" + str(b_act) + " = " + str(round(le2,3))
            Cp_math += "\nle = " + str(round(le,3))
            Fcs = math.prod(Values[4])
            Cp_math += "\nFc*=" + str(Values[1,0]) + "*" + str(Values[1,1]) + "*" + str(Values[1,2]) + "*" + str(Values[1,3]) + "*" + str(Values[1,5]) + "*" + str(Values[0,7]) + " = " + str(Fcs)
            Emin_prime = math.prod(Values[6])
            Cp_math += "\nE_min' = " + str(Values[6,0]) + "*" + str(Values[6,1]) + "*" + str(Values[6,2]) + "*" + str(Values[6,3]) + "*" + str(Values[6,4]) + "*" + str(Values[6,5]) + "*" + str(Values[6,6]) + "*" + str(Values[6,7]) + "*" + str(Values[6,8]) + "*" + str(Values[6,9]) + "*" + str(Values[6,10]) + "*" + str(Values[6,11]) + " = " + str(Emin_prime) + " psi"
            FcE = 0.822*Emin_prime/(le**2)
            Cp_math +="\nFcE = 0.822*Emin'/(le/d)^2     0.822*" + str(Emin_prime) + "/" + str(le) + "^2 = " + str(round(FcE,3))
            F = FcE/Fcs
            Cp_math += "\nF = FcE/Fc*     " + str(round(FcE,3)) + "/" + str(round(Fcs,3)) + " = " + str(round(F,3))
            Cp = (1+F)/(1.6)-(((1+F)/(1.6))**2-F/0.8)**(1/2)
            Cp_math += "\nCp = (1+F)/1.6-√(((1+F)/1.6)^2-F/0.8)     (1+" + str(round(F,3)) + ")/1.6-√(((1+" + str(round(F,3)) + ")/1.6)^2-" + str(round(F,3)) + "/0.8) = " + str(round(Cp,3))
            Values[4,9] = Cp
                
        #getting CT
        CT_math = "Assuming CT = 1"
        Values[6,10] = 1

        #getting Cb
        Cb_math = ""
        Cb_math = ""
        if lb >= 6:
            Cb_math += "lb = " + str(lb) + " ≥ 6 There for Cb=1"
        else:
            Cb = (lb+0.375)/lb
            Cb_math += "Cb = (lb+0.375)/lb     (" + str(lb) + "+0.375)/" + str(lb) + " = " + str(round(Cb,3))
            Values[3,11] = Cb

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
        if Temprature == "T>125F":
            print("Temprature: T≥125")
        elif Temprature == "100F<T<125F":
            print("Temprature: 100≤T<125")
        else:
            print("Temprature: T<100")
        print("Incised: " + incised)
        print("Repetitive member: " + repetitive)
        print("Flat use: " + flat)
        print("length between support: " + str(length) + " ft")
        print("Support: " + Support)
        print("Load: " + load)
        print("Bearing Length: " + str(lb) + " in")

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
        print("CF math: \n" + CF_math)
        print("CL math: \n" + CL_math)
        print("Cp math: \n" + Cp_math)
        print("CT math: \n" + CT_math)
        print("Cb math: \n" + Cb_math)
        for r in range(7):
            print(name_table[r] + " = " + str(Values[r,0]) + "*" + str(Values[r,1]) + "*" + str(Values[r,2]) + "*" + str(Values[r,3]) + "*" + str(Values[r,4]) + "*" + str(Values[r,5]) + "*" + str(Values[r,6]) + "*" + str(Values[r,7]) + "*" + str(Values[r,8]) + "*" + str(Values[r,9]) + "*" + str(Values[r,10]) + "*" + str(Values[r,11]) +" = " + str(new_values[r]) + " psi")
        print (Note)















