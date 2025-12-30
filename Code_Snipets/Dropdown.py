# -*- coding: utf-8 -*-
"""
Created on Wed Nov 19 15:46:06 2025

@author: victo
"""

import sys
from PyQt5.QtWidgets import (
    QApplication, QDialog, QPushButton, QVBoxLayout,
    QComboBox, QHBoxLayout, QLabel
)

class MultiDropDialog(QDialog):
    def __init__(self, questions, options_list):
        super().__init__()
        self.setWindowTitle("Multiple Questions")
        self.setGeometry(1, 30, 600, 400)

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


# Example usage
if __name__ == '__main__':
    questions = [
        "Pick an animal",
        "Pick a number",
        "Pick a color"
    ]

    options_list = [
        ['Cat', 'Dog', 'Hamster', 'Bird'],
        ['1', '2', '3', '4', '5'],
        ['Red', 'Blue', 'Green', 'Yellow']
    ]

    answers = MultiDrop(questions, options_list)
    print("Your selections:", answers)