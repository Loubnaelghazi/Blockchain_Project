import sys
from PyQt5 import QtWidgets
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../')))
from backend.blockchain import Blockchain

class BlockchainApp(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()

        # Initialize the Blockchain class
        self.blockchain = Blockchain()

        # Set up UI
        self.init_ui()

    def init_ui(self):
        # Set up labels
        self.setWindowTitle('Medical Blockchain App')
        self.setGeometry(100, 100, 500, 400)
        self.setStyleSheet("background-color: #f9f9f9; color: #333;")

        self.patient_name_label = QtWidgets.QLabel('Patient Name:', self)
        self.contact_info_label = QtWidgets.QLabel('Contact Info:', self)
        self.insurance_details_label = QtWidgets.QLabel('Insurance Details:', self)
        self.allergies_label = QtWidgets.QLabel('Allergies (comma separated):', self)
        self.chronic_conditions_label = QtWidgets.QLabel('Has Chronic Conditions?', self)

        # Set up input fields
        self.patient_name_input = QtWidgets.QLineEdit(self)
        self.patient_name_input.setStyleSheet(self.input_style())
        self.contact_info_input = QtWidgets.QLineEdit(self)
        self.contact_info_input.setStyleSheet(self.input_style())
        self.insurance_details_input = QtWidgets.QLineEdit(self)
        self.insurance_details_input.setStyleSheet(self.input_style())
        self.allergies_input = QtWidgets.QLineEdit(self)
        self.allergies_input.setStyleSheet(self.input_style())
        self.chronic_conditions_checkbox = QtWidgets.QCheckBox(self)

        # Set up register button
        self.register_button = QtWidgets.QPushButton('Register Patient', self)
        self.register_button.setStyleSheet(self.button_style())
        self.register_button.clicked.connect(self.register_patient)

        # Arrange the layout
        layout = QtWidgets.QFormLayout()
        layout.addRow(self.patient_name_label, self.patient_name_input)
        layout.addRow(self.contact_info_label, self.contact_info_input)
        layout.addRow(self.insurance_details_label, self.insurance_details_input)
        layout.addRow(self.allergies_label, self.allergies_input)
        layout.addRow(self.chronic_conditions_label, self.chronic_conditions_checkbox)
        layout.addWidget(self.register_button)

        self.setLayout(layout)

    def input_style(self):
        return """
        QLineEdit {
            border: 2px solid #4CAF50;
            border-radius: 5px;
            padding: 10px;
            font-size: 14px;
            margin-bottom: 10px;
        }
        QLineEdit:focus {
            border-color: #3e8e41;
        }
        """

    def button_style(self):
        return """
        QPushButton {
            background-color: #4CAF50;
            color: white;
            border: none;
            border-radius: 5px;
            padding: 10px;
            font-size: 16px;
            margin: 10px 0;
        }
        QPushButton:hover {
            background-color: #3e8e41;
        }
        """

    def register_patient(self):
        # Get input values from UI components
        patient_name = self.patient_name_input.text()
        contact_info = self.contact_info_input.text()
        insurance_details = self.insurance_details_input.text()
        allergies = self.allergies_input.text().split(",")  # Convert comma-separated string to list
        has_chronic_conditions = self.chronic_conditions_checkbox.isChecked()

        # Check if all fields are filled
        if patient_name and contact_info and insurance_details and allergies:
            # Register patient by calling the method from Blockchain class
            tx_receipt = self.blockchain.register_patient(
                patient_name,
                contact_info,
                insurance_details,
                allergies,
                has_chronic_conditions
            )
            
            # Handle transaction result
            if tx_receipt:
                QtWidgets.QMessageBox.information(self, 'Success', f'Patient {patient_name} registered successfully!')
            else:
                QtWidgets.QMessageBox.warning(self, 'Error', 'Failed to register patient.')
        else:
            QtWidgets.QMessageBox.warning(self, 'Error', 'Please fill in all required fields.')

