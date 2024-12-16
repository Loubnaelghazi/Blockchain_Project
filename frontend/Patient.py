from PyQt5.QtWidgets import (
    QApplication, QVBoxLayout, QHBoxLayout, QMainWindow, QWidget, QPushButton, QLabel, QStackedWidget
)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont, QPixmap
import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../')))
from backend.blockchain import Blockchain  # Ensure this import matches your actual project structure


class PatientInterface(QMainWindow):
    def __init__(self, patient_address):
        super().__init__()
        self.patient_address = patient_address  # Logged-in patient's Ethereum address
        self.setWindowTitle(f"Patient Dashboard - {self.patient_address}")
        self.setGeometry(100, 100, 1000, 600)
        self.setStyleSheet("background-color: #f4f4f4; color: #333;")
        self.blockchain = Blockchain()  # Blockchain instance
        self.patient_details = {}  # To store fetched patient details
        self.init_ui()
        self.fetch_personal_information()  # Fetch details on initialization

    def init_ui(self):
        # Main Layout
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        main_layout = QHBoxLayout()

        # Sidebar
        self.sidebar = QWidget()
        self.sidebar_layout = QVBoxLayout()
        self.sidebar.setLayout(self.sidebar_layout)
        self.sidebar.setStyleSheet("background-color: #001F3F; color: white; width: 200px;")

        # Sidebar Buttons
        self.home_button = QPushButton("Home")
        self.medical_button = QPushButton("Medical Records")
        self.doctors_button = QPushButton("Doctors")

        self.home_button.setStyleSheet(self.button_style())
        self.medical_button.setStyleSheet(self.button_style())
        self.doctors_button.setStyleSheet(self.button_style())

        self.home_button.clicked.connect(self.show_home)
        self.medical_button.clicked.connect(self.show_records)
        self.doctors_button.clicked.connect(self.show_doctors)

        self.sidebar_layout.addWidget(self.home_button)
        self.sidebar_layout.addWidget(self.medical_button)
        self.sidebar_layout.addWidget(self.doctors_button)

        # Main Content Area
        self.main_content = QStackedWidget()

        # Home Section (Personal Information)
        self.home_layout = QVBoxLayout()
        self.title_label = QLabel("Home")
        self.title_label.setFont(QFont("Arial", 20, QFont.Bold))
        self.title_label.setAlignment(Qt.AlignCenter)
        self.title_label.setStyleSheet("color: #001F3F; margin-bottom: 20px;")
        self.home_layout.addWidget(self.title_label)

        # Patient Avatar and Personal Info
        self.patient_avatar = QLabel()
        self.patient_avatar.setPixmap(QPixmap("patient_avatar.png").scaled(100, 100, Qt.KeepAspectRatio))  # Set avatar image
        self.patient_avatar.setAlignment(Qt.AlignCenter)
        self.home_layout.addWidget(self.patient_avatar)


        self.patient_address_label = QLabel(f"Address: {self.patient_address}")
        self.patient_address_label.setFont(QFont("Arial", 14))
        self.patient_address_label.setStyleSheet("color: #001F3F; margin-bottom: 10px;")
        self.home_layout.addWidget(self.patient_address_label)

        # Personal Info Container
        self.personal_info_container = QWidget()
        self.personal_info_layout = QVBoxLayout()
        self.personal_info_container.setLayout(self.personal_info_layout)
        self.home_layout.addWidget(self.personal_info_container)

        self.home_widget = QWidget()
        self.home_widget.setLayout(self.home_layout)
        self.main_content.addWidget(self.home_widget)

        # Medical Records Section
        self.medicals_widget = QWidget()
        self.medicals_layout = QVBoxLayout()
        self.medicals_widget.setLayout(self.medicals_layout)
        self.main_content.addWidget(self.medicals_widget)


        # Doctors Section
        self.doctors_widget = QWidget()
        self.doctors_layout = QVBoxLayout()
        self.doctors_widget.setLayout(self.doctors_layout)

        self.main_content.addWidget(self.medicals_widget)
        self.main_content.addWidget(self.doctors_widget)

        # Add Sidebar and Main Content Area
        main_layout.addWidget(self.sidebar)
        main_layout.addWidget(self.main_content)
        self.central_widget.setLayout(main_layout)

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
        """Switch to the Home section."""
        self.main_content.setCurrentWidget(self.home_widget)

    def show_records(self):
        """Switch to the Medical Records section and fetch all files."""
        self.main_content.setCurrentWidget(self.medicals_widget)
        self.fetch_and_display_files()

    def show_doctors(self):
        """Switch to the Doctors section and populate the doctor list."""
        self.main_content.setCurrentWidget(self.doctors_widget)
        self.display_doctors()

    def fetch_personal_information(self):
        """Fetch personal information from the blockchain."""
        try:
            # Retrieve the patient's contract address
            patient_contract_address = self.blockchain.get_patient_contract(self.patient_address)
            if patient_contract_address:
                # Fetch patient details using the contract address
                self.patient_details = self.blockchain.get_patient_details(patient_contract_address)
                self.display_personal_information()  # Update the UI with personal details
            else:
                print(f"No contract found for patient address: {self.patient_address}")
        except Exception as e:
            print(f"Error fetching patient information: {e}")

    def display_personal_information(self):
        """Display the patient's personal information in the Home section."""
        # Clear any existing widgets in the layout
        for i in reversed(range(self.personal_info_layout.count())):
            widget = self.personal_info_layout.itemAt(i).widget()
            if widget:
                widget.deleteLater()

        # Populate the layout with fetched patient details
        if self.patient_details:
            for key, value in self.patient_details.items():
                # Create a QLabel with HTML for bold key and normal value
                label = QLabel(f"<b>{key.capitalize()}:</b> {value}")
                label.setFont(QFont("Arial", 14))
                label.setStyleSheet("color: #001F3F; margin-bottom: 5px;")
                self.personal_info_layout.addWidget(label)
        else:
            label = QLabel("No personal information found.")
            label.setFont(QFont("Arial", 14))
            label.setStyleSheet("color: #FF0000; margin-bottom: 5px;")
            self.personal_info_layout.addWidget(label)


    def display_doctors(self):
        """Fetch and display the list of doctors."""
        # Clear the doctors layout
        for i in reversed(range(self.doctors_layout.count())):
            widget = self.doctors_layout.itemAt(i).widget()
            if widget is not None:
                widget.deleteLater()

        # Fetch doctors from the blockchain
        doctors = self.blockchain.get_doctors()

        # Populate the layout with custom widgets for each doctor
        for doctor in doctors:
            doctor_widget = QWidget()
            doctor_layout = QHBoxLayout()

            # Display doctor details
            doctor_label = QLabel(f"{doctor['name']} ({doctor['address']})")
            doctor_label.setFont(QFont("Arial", 14))
            doctor_label.setStyleSheet("color: #001F3F;")

            # Create the "Give Permission" button
            give_permission_button = QPushButton("Give Permission")
            give_permission_button.setStyleSheet(self.button_style())
            give_permission_button.clicked.connect(lambda _, doc=doctor: self.give_permission(doc))

            # Add the label and button to the doctor's layout
            doctor_layout.addWidget(doctor_label)
            doctor_layout.addWidget(give_permission_button)

            # Set the layout and add to the doctors layout
            doctor_widget.setLayout(doctor_layout)
            self.doctors_layout.addWidget(doctor_widget)

    def give_permission(self, doctor):
        """Grant permission to a doctor."""
        try:
            # Set the blockchain default account to the patient address
            self.blockchain.web3.eth.default_account = self.patient_address

            # Log patient and doctor information
            print(f"Granting permission from patient: {self.patient_address} to doctor: {doctor['address']}")

            # Grant permission on the blockchain
            self.blockchain.grant_permission(doctor['address'])
            print(f"Permission granted to {doctor['name']} at address {doctor['address']}.")
        except Exception as e:
            print(f"Error granting permission: {e}")
    
    def grant_permission(self, doctor):
        try:
            self.blockchain.web3.eth.default_account = self.patient_address
            print(f"Granting permission from patient: {self.patient_address} to doctor: {doctor['address']}")
            self.blockchain.grant_permission(doctor['address'])
            print(f"Permission granted to {doctor['name']} at address {doctor['address']}.")
        except Exception as e:
            print(f"Error granting permission: {e}")


    def fetch_and_display_files(self):
        self.clear_layout(self.medicals_layout)

        try:
            # Set the default account to the patient's address
            self.blockchain.web3.eth.default_account = self.patient_address
            print(f"Fetching files with default_account: {self.patient_address}")

            # Fetch all doctors (not just permitted ones)
            all_doctors = self.blockchain.get_doctors()
            print(f"All doctors: {all_doctors}")

            for doctor in all_doctors:
                doctor_address = doctor["address"]
                doctor_contract_address = self.blockchain.get_doctor_contract(doctor_address)
                print(f"Doctor contract for {doctor_address}: {doctor_contract_address}")

                if doctor_contract_address:
                    # Fetch files from the doctor's contract for the patient
                    files = self.blockchain.get_patient_files(doctor_contract_address, self.patient_address)
                    print(f"Files from doctor {doctor_address}: {files}")

                    if files:
                        for file in files:
                            file_name = file["fileName"]
                            file_hash = file["fileHash"]
                            ipfs_link = f"http://localhost:8080/ipfs/{file_hash}"

                            file_link = QLabel(f'<a href="{ipfs_link}" style="color: blue;">{file_name}</a>')
                            file_link.setOpenExternalLinks(True)
                            self.medicals_layout.addWidget(file_link)
                    else:
                        self.medicals_layout.addWidget(QLabel(f"No files uploaded by doctor {doctor_address}."))

        except Exception as e:
            self.medicals_layout.addWidget(QLabel(f"Error fetching medical records: {e}"))
            print(f"Error fetching medical records: {e}")







    def clear_layout(self, layout):
        """Remove all widgets from a layout."""
        while layout.count():
            item = layout.takeAt(0)
            widget = item.widget()
            if widget is not None:
                widget.deleteLater()
            else:
                # If it's a layout, recursively clear it
                self.clear_layout(item.layout())








if __name__ == "__main__":
    app = QApplication(sys.argv)
    # Replace "0xYourPatientAddress" with the Ethereum address of the logged-in patient
    patient_address = "0xYourPatientAddress"  # This will come dynamically from the login form
    window = PatientInterface(patient_address)
    window.show()
    sys.exit(app.exec_())
