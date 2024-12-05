import sys
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QPushButton, QVBoxLayout, QHBoxLayout, QWidget,
    QLabel, QLineEdit
)
from PyQt5.QtGui import QFont
from PyQt5.QtCore import Qt
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../')))
from backend.blockchain import Blockchain

class AuditInterface(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Audit - User Management")
        self.setGeometry(100, 100, 800, 600)
        self.setStyleSheet("background-color: #f4f4f4; color: #333;")
        self.blockchain = Blockchain()  # Instance du backend blockchain
        self.init_ui()

    def init_ui(self):
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)

        self.main_layout = QVBoxLayout()

        self.title_label = QLabel("Audit - User Management")
        self.title_label.setFont(QFont("Arial", 20, QFont.Bold))
        self.title_label.setAlignment(Qt.AlignCenter)
        self.title_label.setStyleSheet("color: #4CAF50; margin-bottom: 20px;")
        self.main_layout.addWidget(self.title_label)

        self.button_layout = QHBoxLayout()
        self.add_patient_button = QPushButton("Add Patient")
        self.add_patient_button.setStyleSheet(self.button_style())
        self.add_patient_button.clicked.connect(self.show_patient_form)
        self.button_layout.addWidget(self.add_patient_button)

        self.add_doctor_button = QPushButton("Add Doctor")
        self.add_doctor_button.setStyleSheet(self.button_style())
        self.add_doctor_button.clicked.connect(self.show_doctor_form)
        self.button_layout.addWidget(self.add_doctor_button)

        self.main_layout.addLayout(self.button_layout)

        self.form_container = QWidget()
        self.form_layout = QVBoxLayout()
        self.form_container.setLayout(self.form_layout)
        self.main_layout.addWidget(self.form_container)

        self.central_widget.setLayout(self.main_layout)

    def button_style(self):
        return """
        QPushButton {
            background-color: #4CAF50;
            color: white;
            border: none;
            border-radius: 5px;
            padding: 10px 20px;
            font-size: 16px;
            margin: 10px;
        }
        QPushButton:hover {
            background-color: #3e8e41;
        }
        """

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

    def clear_form(self):
        for i in reversed(range(self.form_layout.count())):
            widget = self.form_layout.itemAt(i).widget()
            if widget is not None:
                widget.deleteLater()

    def submit_user_form(self, role):
        """
        Soumet un formulaire pour ajouter un utilisateur avec un rôle spécifique (Patient ou Docteur).
        :param role: 0 pour Patient, 1 pour Docteur.
        """
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

