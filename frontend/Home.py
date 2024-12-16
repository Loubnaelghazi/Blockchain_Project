import os
import json
from web3 import Web3
import sys
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QPushButton,
    QLabel, QStackedWidget, QLineEdit, QDialog
)
from PyQt5.QtGui import QFont, QPixmap
from PyQt5.QtCore import Qt

from main import AuditInterface  # Import the AuditInterface class
from Patient import PatientInterface
from Doctor import DoctorInterface

# Connect to Ganache
ganache_url = "http://127.0.0.1:7545"  # Replace with your Ganache RPC URL
web3 = Web3(Web3.HTTPProvider(ganache_url))

# Load ABI dynamically from the JSON file
current_dir = os.path.dirname(os.path.abspath(__file__))  # Get current script directory
audit_file_path = os.path.join(current_dir, "../build/contracts/AuditContract.json")  # Path to the compiled contract JSON

with open(audit_file_path, "r") as file:
    audit_contract_info = json.load(file)  # Load JSON file
    contract_abi = audit_contract_info["abi"]  # Extract ABI

# Replace with your deployed contract address
contract_address = "0x8b5f29Ea69bc4Ff5239B10282346d5820D65207c"

# Load the contract
contract = web3.eth.contract(address=contract_address, abi=contract_abi)

# Hardcoded admin address and private key
admin_address = "0x5D4281e40bEf3E5944144C87095a6E7C8bBD28E6"
admin_private_key = "admin"


class LoginForm(QWidget):
    def __init__(self, role):
        super().__init__()
        self.role = role
        self.setWindowTitle(f"Login Form - {role}")
        self.setFixedSize(400, 500)
        self.init_ui()

    def init_ui(self):
        self.setStyleSheet("""
            QWidget {
                background-color: #F7DBFF;
            }
            QLabel {
                font-family: Arial;
                color: #001F3F;
            }
            QPushButton {
                background-color: #001F3F;
                color: white;
                font-size: 16px;
                padding: 10px;
                border: none;
                border-radius: 5px;
            }
            QPushButton:hover {
                background-color: #001F3F;
            }
            QLineEdit {
                padding: 10px;
                border: 1px solid #ccc;
                border-radius: 5px;
                font-size: 16px;
            }
        """)

        main_layout = QVBoxLayout(self)

        # Title
        title = QLabel(f"Login as {self.role}")
        title.setFont(QFont("Arial", 24, QFont.Bold))
        title.setAlignment(Qt.AlignCenter)
        title.setStyleSheet("margin-bottom: 20px;")
        main_layout.addWidget(title)

        # Ethereum Address Field
        self.address_field = QLineEdit()
        self.address_field.setPlaceholderText("Ethereum Address")
        main_layout.addWidget(self.address_field)

        # Private Key Field
        self.private_key_field = QLineEdit()
        self.private_key_field.setPlaceholderText("Private Key")
        self.private_key_field.setEchoMode(QLineEdit.Password)
        main_layout.addWidget(self.private_key_field)

        # Login Button
        login_button = QPushButton("Login")
        login_button.clicked.connect(self.handle_login)
        main_layout.addWidget(login_button)

        # Back Link
        signup_label = QLabel("Back? <a href='#' style='color: #001F3F;'>Click Here</a>")
        signup_label.setAlignment(Qt.AlignCenter)
        signup_label.setTextInteractionFlags(Qt.TextBrowserInteraction)
        signup_label.linkActivated.connect(self.back_to_home)
        main_layout.addWidget(signup_label)

    def handle_login(self):
        user_address = self.address_field.text()
        private_key = self.private_key_field.text()

        if not web3.is_address(user_address):
            self.show_message("Invalid Ethereum address")
            return

        try:
            # Check if the user is the admin
            if user_address == admin_address and private_key == admin_private_key:
                self.show_audit_interface()
                return

            # Check user role
            user_data = contract.functions.users(user_address).call()
            print(f"User Data: {user_data}")

            is_registered = user_data[3]  # Assuming isRegistered is at index 3
            role = user_data[2]  # Assuming role is at index 2

            if not is_registered:
                self.show_message("User is not registered")
            else:
                if role == 0:  # Patient
                    if self.role == "Patient":
                        self.show_patient_interface(user_address)  # Pass user_address
                    else:
                        self.show_message("Sorry, this form is just for patients.")
                elif role == 1:  # Doctor
                    if self.role == "Doctor":
                        self.show_doctor_interface(user_address)  # Pass the doctor's Ethereum address
                    else:
                        self.show_message("Sorry, this form is just for doctors.")
                else:
                    self.show_message("Unknown role")

        except Exception as e:
            self.show_message(f"Error: {str(e)}")

    def show_patient_interface(self, user_address):
        """Navigate to the Patient Interface with the given user_address."""
        self.patient_interface = PatientInterface(user_address)  # Pass user_address to PatientInterface
        self.patient_interface.show()
        self.close()

    def show_message(self, message):
        dialog = QDialog(self)
        dialog.setWindowTitle("Message")
        layout = QVBoxLayout(dialog)
        label = QLabel(message)
        layout.addWidget(label)
        dialog.exec_()

    def back_to_home(self):
        """Navigate back to the home page."""
        self.home_page = Home()
        self.home_page.show()
        self.close()

    def show_audit_interface(self):
        """Navigate to the Audit Interface."""
        self.audit_interface = AuditInterface()
        self.audit_interface.show()
        self.close()

    def show_doctor_interface(self, doctor_address):
        """Navigate to the Doctor Interface with the given doctor address."""
        self.doctor_interface = DoctorInterface(doctor_address)  # Pass doctor_address
        self.doctor_interface.show()
        self.close()



class Home(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Welcome")
        self.setGeometry(100, 100, 1200, 800)  # Dimensions of the window
        self.init_ui()

    def init_ui(self):
        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        main_layout = QVBoxLayout(central_widget)
        main_layout.setContentsMargins(0, 0, 0, 0)

        # Header Section (Navigation Bar)
        header_layout = QHBoxLayout()
        header_layout.setContentsMargins(20, 10, 20, 10)

        # Navigation Bar Buttons
        nav_items = ["Medical App"]
        for item in nav_items:
            nav_button = QPushButton(item)
            nav_button.setStyleSheet("""
                QPushButton {
                    background-color: transparent;
                    color: #001F3F;
                    font-size: 26px;
                    border: none;
                    margin: 0 10px;
                }
                QPushButton:hover {
                    color: #000;
                }
            """)
            nav_button.clicked.connect(lambda _, x=item: self.show_login_form(x))
            header_layout.addWidget(nav_button)

        header_layout.addStretch()
        main_layout.addLayout(header_layout)

        # Stacked Widget to switch between home and login
        self.stacked_widget = QStackedWidget()
        main_layout.addWidget(self.stacked_widget)

        # Home Page
        home_page = QWidget()
        home_layout = QHBoxLayout(home_page)
        home_layout.setContentsMargins(0, 0, 0, 0)

        # Left half: Background Image
        left_half = QLabel()
        background_pixmap = QPixmap("images.jpg").scaled(600, 800, Qt.KeepAspectRatioByExpanding, Qt.SmoothTransformation)
        left_half.setPixmap(background_pixmap)
        left_half.setStyleSheet("background-color: #001F3F;")
        left_half.setFixedWidth(600)

        # Right half: Dark Blue Background
        right_half = QWidget()
        right_half.setStyleSheet("background-color: #001F3F;")
        right_half_layout = QVBoxLayout(right_half)
        right_half_layout.setAlignment(Qt.AlignCenter)

        # Title and Subtitle
        title_label = QLabel("Unlimited Access to Your Application")
        title_label.setFont(QFont("Arial", 28, QFont.Bold))
        title_label.setStyleSheet("color: white;")
        title_label.setAlignment(Qt.AlignCenter)

        subtitle_label = QLabel("The perfect care for you with the best professionals.")
        subtitle_label.setFont(QFont("Arial", 14))
        subtitle_label.setStyleSheet("color: white; margin-top: 10px;")
        subtitle_label.setWordWrap(True)
        subtitle_label.setAlignment(Qt.AlignCenter)

        # Call-to-Action Buttons (Patient and Doctor)
        buttons_layout = QHBoxLayout()
        startP_button = QPushButton("Start as a Patient")
        startP_button.setStyleSheet("""
            QPushButton {
                background-color: #fff;
                color: #001F3F;
                font-size: 16px;
                padding: 15px 30px;
                border-radius: 5px;
                border: none;
                margin-top: 20px;
            }
            QPushButton:hover {
                background-color: #fff;
            }
        """)
        startP_button.clicked.connect(lambda: self.show_login_form("Patient"))

        startD_button = QPushButton("Start as a Doctor")
        startD_button.setStyleSheet("""
            QPushButton {
                background-color: #fff;
                color: #001F3F;
                font-size: 16px;
                padding: 15px 30px;
                border-radius: 5px;
                border: none;
                margin-top: 20px;
            }
            QPushButton:hover {
                background-color: #fff;
            }
        """)
        startD_button.clicked.connect(lambda: self.show_login_form("Doctor"))

        buttons_layout.addWidget(startP_button)
        buttons_layout.addWidget(startD_button)

        right_half_layout.addWidget(title_label)
        right_half_layout.addWidget(subtitle_label)
        right_half_layout.addLayout(buttons_layout)

        # Adding both halves to home layout
        home_layout.addWidget(left_half)
        home_layout.addWidget(right_half)

        self.stacked_widget.addWidget(home_page)

    def show_login_form(self, role):
        self.login_form = LoginForm(role)
        self.login_form.show()
        self.close()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = Home()
    window.show()
    sys.exit(app.exec_())
