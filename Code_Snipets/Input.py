import sys
from PyQt5.QtWidgets import QApplication, QDialog, QPushButton, QVBoxLayout, QLabel, QLineEdit, QMessageBox, QInputDialog

class InputDialog(QDialog):
    def __init__(self, question):
        super().__init__()
        self.setWindowTitle(question)
        self.setGeometry(1, 30, 1060, 960)
        self.selected_option = None  # This will store the selected value

        layout = QVBoxLayout()

        # Show the question
        self.label = QLabel(question)
        layout.addWidget(self.label)

        # Add text input field
        self.text_input = QLineEdit()
        layout.addWidget(self.text_input)

        # Add a submit button
        submit_button = QPushButton("Submit")
        submit_button.clicked.connect(self.submit_input)
        layout.addWidget(submit_button)
        
        # Add a cancel button
        cancel_button = QPushButton("Cancel")
        cancel_button.clicked.connect(self.cancel_input)
        layout.addWidget(cancel_button)

        self.setLayout(layout)

    def submit_input(self):
        self.selected_option = self.text_input.text()
        self.accept()  # Close the dialog and mark it as accepted
    
    def cancel_input(self):
        self.selected_option = None
        self.reject()  # Close the dialog and mark it as rejected

def Input(question):
    app = QApplication.instance() or QApplication(sys.argv)
    dialog = InputDialog(question)
    result = dialog.exec_()
    if result == QDialog.Accepted:
        return dialog.selected_option
    else:
        sys.exit()  # User canceled the dialog

    
question = "Pick an animal"
if __name__ == '__main__':
    animal = Input(question)

question = "Pick an number"
if __name__ == '__main__':
    number = Input(question)