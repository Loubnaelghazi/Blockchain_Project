from PyQt5.QtWidgets import QVBoxLayout, QHBoxLayout, QMainWindow, QWidget, QPushButton, QLabel, QLineEdit, QStackedWidget, QFrame, QListWidget, QComboBox, QTableWidget, QTableWidgetItem, QHeaderView
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont
from datetime import datetime
import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../')))
from backend.blockchain import Blockchain

class AuditInterface(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Audit - User Management")
        self.setGeometry(100, 100, 1000, 600)
        self.setStyleSheet("background-color: #f4f4f4; color: #333;")
        self.blockchain = Blockchain()
        self.init_ui()

    def init_ui(self):
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)

        # Main Layout
        main_layout = QHBoxLayout()

        # Sidebar
        self.sidebar = QWidget()
        self.sidebar_layout = QVBoxLayout()
        self.sidebar.setLayout(self.sidebar_layout)
        self.sidebar.setStyleSheet("background-color: #001F3F; color: white; width: 200px;")
        
        # Sidebar Buttons (Home, Patients, Doctors, Transactions)
        self.home_button = QPushButton("Home")
        self.patients_button = QPushButton("Patients")
        self.doctors_button = QPushButton("Doctors")
        self.transactions_button = QPushButton("Transactions")  # Fixed indentation

        # Apply button styling
        self.home_button.setStyleSheet(self.button_style())
        self.patients_button.setStyleSheet(self.button_style())
        self.doctors_button.setStyleSheet(self.button_style())
        self.transactions_button.setStyleSheet(self.button_style())  # Added styling

        # Connect buttons to their respective functions
        self.home_button.clicked.connect(self.show_home)
        self.patients_button.clicked.connect(self.show_patients)
        self.doctors_button.clicked.connect(self.show_doctors)
        self.transactions_button.clicked.connect(self.display_transactions_section)  # Connect Transactions button

        # Add buttons to sidebar layout
        self.sidebar_layout.addWidget(self.home_button)
        self.sidebar_layout.addWidget(self.patients_button)
        self.sidebar_layout.addWidget(self.doctors_button)
        self.sidebar_layout.addWidget(self.transactions_button)  # Add Transactions button


        # Main Content Area
        self.main_content = QStackedWidget()

        # Home Section (with Add Patient and Add Doctor buttons)
        self.home_layout = QVBoxLayout()
        self.title_label = QLabel("Audit - User Management")
        self.title_label.setFont(QFont("Arial", 20, QFont.Bold))
        self.title_label.setAlignment(Qt.AlignCenter)
        self.title_label.setStyleSheet("color: #001F3F; margin-bottom: 20px;")
        self.home_layout.addWidget(self.title_label)

        self.button_layout = QHBoxLayout()
        self.add_patient_button = QPushButton("Add Patient")
        self.add_patient_button.setStyleSheet(self.button_style())
        self.add_patient_button.clicked.connect(self.show_patient_form)
        self.button_layout.addWidget(self.add_patient_button)

        self.add_doctor_button = QPushButton("Add Doctor")
        self.add_doctor_button.setStyleSheet(self.button_style())
        self.add_doctor_button.clicked.connect(self.show_doctor_form)
        self.button_layout.addWidget(self.add_doctor_button)

        self.home_layout.addLayout(self.button_layout)

        self.form_container = QWidget()
        self.form_layout = QVBoxLayout()
        self.form_container.setLayout(self.form_layout)
        self.home_layout.addWidget(self.form_container)

        self.home_widget = QWidget()
        self.home_widget.setLayout(self.home_layout)

        # Add the home widget to the stacked widget
        self.main_content.addWidget(self.home_widget)
        
        # Add the sidebar and main content area to the main layout
        main_layout.addWidget(self.sidebar)
        main_layout.addWidget(self.main_content)

        self.central_widget.setLayout(main_layout)

        # Patients Section
        self.patients_widget = QWidget()
        self.patients_layout = QVBoxLayout()
        self.patients_list = QListWidget()  # List to display patients
        self.patients_layout.addWidget(self.patients_list)
        self.patients_widget.setLayout(self.patients_layout)

        # Doctors Section
        self.doctors_widget = QWidget()
        self.doctors_layout = QVBoxLayout()
        self.doctors_list = QListWidget()  # List to display doctors
        self.doctors_layout.addWidget(self.doctors_list)
        self.doctors_widget.setLayout(self.doctors_layout)

        # Add the home widget to the stacked widget
        self.main_content.addWidget(self.home_widget)

        # Add the patients and doctors widgets to the stacked widget
        self.main_content.addWidget(self.patients_widget)
        self.main_content.addWidget(self.doctors_widget)
        



    def button_style(self):
        return """
        QPushButton {
            background-color: #001F3F;
            color: white;
            border: none;
            border-radius: 5px;
            padding: 10px 20px;
            font-size: 16px;
            margin: 10px;
        }
        QPushButton:hover {
            background-color: #003366;
        }
        """
    
    def show_home(self):
        self.main_content.setCurrentWidget(self.home_widget)

    def show_patients(self):
        self.main_content.setCurrentWidget(self.patients_widget)
        self.display_patients()

    def show_doctors(self):
        self.main_content.setCurrentWidget(self.doctors_widget)
        self.display_doctors()
    
    

    def display_patients(self):
        self.patients_list.clear()
        self.patients = self.blockchain.get_patients()

        for patient in self.patients:
            self.patients_list.addItem(f"{patient['name']} ({patient['address']})")
        
        # Disconnect any existing signal connections to prevent duplicates
        try:
            self.patients_list.itemClicked.disconnect()
        except TypeError:
            pass

        # Connect the signal to the handler
        self.patients_list.itemClicked.connect(self.show_patient_details_form)


    def display_doctors(self):
        # Clear the doctors list widget
        self.doctors_list.clear()

        # Fetch doctors from the blockchain
        doctors = self.blockchain.get_doctors()

        # Populate the QListWidget
        for doctor in doctors:
            self.doctors_list.addItem(f"{doctor['name']} ({doctor['address']})")


    def show_patient_form(self):
        self.clear_form()
        self.title_label.setText("Add a Patient")
        self.name_input = QLineEdit()
        self.name_input.setPlaceholderText("Patient Name")
        self.name_input.setStyleSheet(self.input_style())
        self.form_layout.addWidget(self.name_input)

        self.wallet_input = QLineEdit()
        self.wallet_input.setPlaceholderText("Ethereum Address")
        self.wallet_input.setStyleSheet(self.input_style())
        self.form_layout.addWidget(self.wallet_input)

        self.submit_button = QPushButton("Save Patient")
        self.submit_button.setStyleSheet(self.button_style())
        self.submit_button.clicked.connect(lambda: self.submit_user_form(0))  # Role 0 pour Patient
        self.form_layout.addWidget(self.submit_button)

    def show_doctor_form(self):
        self.clear_form()
        self.title_label.setText("Add a Doctor")
        self.name_input = QLineEdit()
        self.name_input.setPlaceholderText("Doctor Name")
        self.name_input.setStyleSheet(self.input_style())
        self.form_layout.addWidget(self.name_input)

        self.wallet_input = QLineEdit()
        self.wallet_input.setPlaceholderText("Ethereum Address")
        self.wallet_input.setStyleSheet(self.input_style())
        self.form_layout.addWidget(self.wallet_input)

        self.submit_button = QPushButton("Save Doctor")
        self.submit_button.setStyleSheet(self.button_style())
        self.submit_button.clicked.connect(lambda: self.submit_user_form(1))  # Role 1 pour Doctor
        self.form_layout.addWidget(self.submit_button)

    def input_style(self):
        return """
        QLineEdit {
            border: 2px solid #001F3F;
            border-radius: 5px;
            padding: 10px;
            font-size: 14px;
            margin-bottom: 10px;
        }
        QLineEdit:focus {
            border-color: #001F3F;
        }
        """

    def clear_form(self):
        current_layout = self.form_container.layout()
        if current_layout is not None:
            # Remove all child widgets from the layout
            while current_layout.count():
                child = current_layout.takeAt(0)
                if child.widget():
                    child.widget().deleteLater()



    def submit_user_form(self, role):
        name = self.name_input.text()
        wallet = self.wallet_input.text()

        if not name or not wallet:
            print("Veuillez remplir tous les champs.")
            return

        if not wallet.startswith("0x") or len(wallet) != 42:
            print("Adresse Ethereum invalide.")
            return

        try:
            receipt = self.blockchain.register_user(wallet, name, role=role)
            print(f"Utilisateur {name} enregistré avec succès. Transaction: {receipt}")
        except Exception as e:
            print(f"Erreur lors de l'enregistrement : {e}")
    

    def show_patient_details_form(self, data):
        if isinstance(data, dict):  # Called after saving updated details
            patient_address = data.get("patientAddress", "")
            current_details = data
            patient_contract_address = self.blockchain.get_patient_contract(patient_address)
        else:  # Called from QListWidgetItem
            patient_address = data.text().split("(")[1][:-1].strip()
            patient_contract_address = self.blockchain.get_patient_contract(patient_address)

            if not patient_contract_address or patient_contract_address == "0x0000000000000000000000000000000000000000":
                print(f"No valid contract found for patient: {patient_address}")
                return

            # Fetch existing details from the blockchain
            try:
                current_details = self.blockchain.get_patient_details(patient_contract_address)
                print(f"Fetched patient details: {current_details}")
            except Exception as e:
                print(f"Error fetching patient details: {e}")
                return

        # Clear the form before adding new widgets
        self.clear_form()

        # Populate the form fields
        self.user_name_input = QLineEdit()
        self.user_name_input.setText(patient_address)
        self.user_name_input.setReadOnly(True)

        self.gender_input = QComboBox()
        self.gender_input.addItems(["Male", "Female", "Other"])
        if "gender" in current_details and current_details["gender"]:
            index = self.gender_input.findText(current_details["gender"], Qt.MatchFixedString)
            if index >= 0:
                self.gender_input.setCurrentIndex(index)

        self.dob_input = QLineEdit(current_details.get("date of birth", "YYYY-MM-DD"))
        self.blood_type_input = QLineEdit(current_details.get("bloodType", "Enter Blood Type"))
        self.phone_input = QLineEdit(current_details.get("phone", "Enter Phone Number"))
        self.address_input = QLineEdit(current_details.get("addressInfo", "Enter Address Info"))
        self.allergies_input = QLineEdit(current_details.get("allergies", "Enter Allergies"))
        self.medical_conditions_input = QLineEdit(current_details.get("medicalConditions", "Enter Medical Conditions"))
        self.notes_input = QLineEdit(current_details.get("notes", "Enter Notes"))

        # Add form labels and inputs to the layout
        form_layout = self.form_container.layout()
        form_layout.addWidget(QLabel("Patient Address:"))
        form_layout.addWidget(self.user_name_input)
        form_layout.addWidget(QLabel("Gender:"))
        form_layout.addWidget(self.gender_input)
        form_layout.addWidget(QLabel("Date of Birth:"))
        form_layout.addWidget(self.dob_input)
        form_layout.addWidget(QLabel("Blood Type:"))
        form_layout.addWidget(self.blood_type_input)
        form_layout.addWidget(QLabel("Phone:"))
        form_layout.addWidget(self.phone_input)
        form_layout.addWidget(QLabel("Address Info:"))
        form_layout.addWidget(self.address_input)
        form_layout.addWidget(QLabel("Allergies:"))
        form_layout.addWidget(self.allergies_input)
        form_layout.addWidget(QLabel("Medical Conditions:"))
        form_layout.addWidget(self.medical_conditions_input)
        form_layout.addWidget(QLabel("Notes:"))
        form_layout.addWidget(self.notes_input)

        # Add the save button to register patient details
        record_button = QPushButton("Save Details")
        record_button.setStyleSheet(self.button_style())
        record_button.clicked.connect(lambda: self.save_patient_details(patient_contract_address))
        form_layout.addWidget(record_button)

        # Ensure the form is visible
        self.main_content.setCurrentWidget(self.home_widget)


    def save_patient_details(self, patient_contract_address):
        details = {
            "gender": self.gender_input.currentText(),
            "date of birth": self.dob_input.text(),
            "bloodType": self.blood_type_input.text(),
            "phone": self.phone_input.text(),
            "addressInfo": self.address_input.text(),
            "notes": self.notes_input.text(),
            "medicalConditions": self.medical_conditions_input.text(),
            "allergies": self.allergies_input.text(),
        }
        try:
            # Update details in the blockchain
            self.blockchain.update_patient_details(patient_contract_address, details)
            print(f"Details for patient at {patient_contract_address} updated successfully.")
            
            # Fetch and refresh the updated details
            updated_details = self.blockchain.get_patient_details(patient_contract_address)
            print(f"Updated details: {updated_details}")
            
            # Call show_patient_details_form with the updated details
            updated_details["patientAddress"] = self.user_name_input.text()  # Add address to details
            self.show_patient_details_form(updated_details)
        except Exception as e:
            print(f"Error updating patient details: {e}")


    def display_transactions_section(self):
        # Clear the main content area
        self.clear_main_content()

        # Set up the transactions section
        transactions_layout = QVBoxLayout()
        transactions_label = QLabel("Doctor-Patient Transactions")
        transactions_label.setStyleSheet("font-size: 18px; font-weight: bold; margin: 10px;")
        transactions_layout.addWidget(transactions_label)

        transactions_table = QTableWidget()
        transactions_table.setColumnCount(4)
        transactions_table.setHorizontalHeaderLabels(["Patient Address", "Doctor Address", "Timestamp", "Details"])
        transactions_layout.addWidget(transactions_table)

        try:
            blockchain = Blockchain()

            # Fetch all patients
            patients = blockchain.get_patients()
            print(f"Fetched patients: {patients}")

            all_transactions = []

            # Iterate through patients and fetch their transactions
            for patient in patients:
                patient_address = patient["address"]
                print(f"Fetching permitted doctors for patient: {patient_address}")
                permitted_doctors = blockchain.get_permitted_patients(patient_address)
                print(f"Permitted doctors for {patient_address}: {permitted_doctors}")

                for doctor_address in permitted_doctors:
                    print(f"Fetching transactions between {patient_address} and {doctor_address}")
                    transactions = blockchain.get_transaction_history(patient_address, doctor_address)
                    print(f"Transactions: {transactions}")

                    for tx in transactions:
                        all_transactions.append({
                            "patient": patient_address,
                            "doctor": doctor_address,
                            "timestamp": tx["timestamp"],
                            "details": tx["details"],
                        })

            # Populate the table
            transactions_table.setRowCount(len(all_transactions))
            for row, tx in enumerate(all_transactions):
                transactions_table.setItem(row, 0, QTableWidgetItem(tx["patient"]))
                transactions_table.setItem(row, 1, QTableWidgetItem(tx["doctor"]))
                transactions_table.setItem(row, 2, QTableWidgetItem(str(tx["timestamp"])))
                transactions_table.setItem(row, 3, QTableWidgetItem(tx["details"]))

        except Exception as e:
            error_label = QLabel(f"Error fetching transactions: {e}")
            error_label.setStyleSheet("color: red;")
            transactions_layout.addWidget(error_label)

        # Add the transactions layout to the main content
        transactions_widget = QWidget()
        transactions_widget.setLayout(transactions_layout)
        self.main_content.addWidget(transactions_widget)
        self.main_content.setCurrentWidget(transactions_widget)




    def clear_main_content(self):
        """Clear all widgets from the main content area."""
        current_widget = self.main_content.currentWidget()
        if current_widget:
            # Remove all child widgets from the layout of the current widget
            layout = current_widget.layout()
            if layout:
                while layout.count():
                    child = layout.takeAt(0)
                    if child.widget():
                        child.widget().deleteLater()


