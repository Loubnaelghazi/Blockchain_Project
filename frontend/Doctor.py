import sys
from PyQt5.QtWidgets import (
    QApplication,
    QMainWindow,
    QLabel,
    QVBoxLayout,
    QWidget,
    QStackedWidget,
    QFrame,
    QHBoxLayout,
    QFileDialog,
    QGroupBox,
    QPushButton
)
from PyQt5.QtGui import QFont, QIcon, QPixmap
from PyQt5.QtCore import QSize, Qt  # Add this line to import Qt
from backend.blockchain import Blockchain
import ipfshttpclient
from functools import partial



class DoctorInterface(QMainWindow):
    def __init__(self, doctor_address):
        super().__init__()
        self.setWindowTitle("Doctor Dashboard")
        self.setGeometry(100, 100, 900, 600)
        self.setStyleSheet("background-color: #f9f9f9; color: #333;")

        # Store the doctor's Ethereum address
        self.doctor_address = doctor_address  # Store the doctor's Ethereum address
        self.blockchain = Blockchain(doctor_address=doctor_address)
        
        # To store doctor's details fetched from the blockchain
        self.doctor_details = {}
        
        # To store the currently selected patient's address
        self.selected_patient_address = None

        # Initialize UI and fetch doctor's information
        self.init_ui()
        self.fetch_doctor_information()

    def init_ui(self):
        # Main layout
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        main_layout = QHBoxLayout()

        # Sidebar
        sidebar_layout = QVBoxLayout()
        sidebar = QFrame()
        sidebar.setFrameShape(QFrame.StyledPanel)
        sidebar.setStyleSheet(self.sidebar_style())
        sidebar.setFixedWidth(250)

        # Sidebar buttons
        home_button = self.create_sidebar_button("Home", "home_icon.png", self.show_home)
        medical_record_button = self.create_sidebar_button("Medical Record", "file_icon.png", self.show_medical_record)
        patients_button = self.create_sidebar_button("Patients", "patient_icon.png", self.show_patients)

        sidebar_layout.addWidget(home_button)
        sidebar_layout.addWidget(medical_record_button)
        sidebar_layout.addWidget(patients_button)

        sidebar.setLayout(sidebar_layout)

        # StackedWidget for sections
        self.stacked_widget = QStackedWidget()
        self.home_page = self.create_home_page()
        self.stacked_widget.addWidget(self.home_page)
        self.stacked_widget.addWidget(self.create_medical_record_page())
        self.stacked_widget.addWidget(self.create_patients_page())

        # Add sidebar and stacked widget to the main layout
        main_layout.addWidget(sidebar)
        main_layout.addWidget(self.stacked_widget)
        central_widget.setLayout(main_layout)

    def sidebar_style(self):
        return """
        QFrame {
            background-color: #001F3F;
            color: white;
            border-right: 2px solid #001F3F;
        }
        QPushButton {
            background-color: #001F3F;
            color: white;
            border: none;
            padding: 5px 10px;
            font-size: 16px;
            text-align: left;
            border-bottom: 1px solid #001F3F;
        }
        QPushButton:hover {
            background-color: #001F3F;
            color: white;
        }
        QPushButton:focus {
            outline: none;
        }
        """

    def create_sidebar_button(self, text, icon_path, callback):
        button = QPushButton(text)
        button.setStyleSheet("""
            QPushButton {
                background-color: #001F3F;
                color: white;
                border: none;
                padding: 5px 10px;
                font-size: 16px;
                text-align: left;
                border-bottom: 1px solid #001F3F;
            }
            QPushButton:hover {
                background-color: #001F3F;
                color: white;
            }
            QPushButton:focus {
                outline: none;
            }
        """)
        button.setIcon(QIcon(icon_path))
        button.setIconSize(QSize(20, 20))
        button.clicked.connect(callback)
        return button

    def create_home_page(self):
        """Create the Home Page with Doctor's Details."""
        home_page = QWidget()
        layout = QVBoxLayout()

        # Title
        self.home_label = QLabel("")
        self.home_label.setFont(QFont("Arial", 18, QFont.Bold))
        layout.addWidget(self.home_label)

        # Doctor's Avatar
        self.avatar_label = QLabel()
        avatar_pixmap = QPixmap("doctor_avatar.png")  # Path to the avatar image
        self.avatar_label.setPixmap(avatar_pixmap.scaled(100, 100))  # Resize the avatar image if necessary
        self.avatar_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(self.avatar_label)

        # Doctor's Name
        self.doctor_name_label = QLabel("Loading doctor's name...")
        self.doctor_name_label.setFont(QFont("Arial", 14, QFont.Bold))
        self.doctor_name_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(self.doctor_name_label)

        # Doctor's Address
        self.doctor_address_label = QLabel("Loading doctor's address...")
        self.doctor_address_label.setFont(QFont("Arial", 12))
        self.doctor_address_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(self.doctor_address_label)

        home_page.setLayout(layout)
        return home_page


    def show_patients(self):
        """Fetch and display patients who granted permission to the logged-in doctor."""
        self.stacked_widget.setCurrentIndex(2)  # Switch to Patients page
        self.clear_layout(self.patients_page.layout())  # Clear previous widgets

        try:
            # Fetch permitted patients from the blockchain
            permitted_patients = self.blockchain.get_permitted_patients(self.doctor_address)

            if not permitted_patients:
                no_patients_label = QLabel("No patients have granted you permission.")
                no_patients_label.setFont(QFont("Arial", 14))
                no_patients_label.setStyleSheet("color: #FF0000;")
                self.patients_page.layout().addWidget(no_patients_label)
                return

            # Fetch and display each patient's personal information
            for patient_address in permitted_patients:
                # Fetch patient contract address
                patient_contract_address = self.blockchain.get_patient_contract(patient_address)
                
                # Fetch personal details from the patient's contract
                patient_details = self.blockchain.get_patient_details(patient_contract_address)
                
                # Create a display widget for each patient
                patient_widget = QWidget()
                patient_layout = QVBoxLayout()

                # Add patient details to the layout
                patient_info = (
                    f"Address: {patient_address}\n"
                    f"Gender: {patient_details.get('gender')}\n"
                    f"DOB: {patient_details.get('dob')}\n"
                    f"Blood Type: {patient_details.get('bloodType')}\n"
                    f"Medical Conditions: {patient_details.get('medicalConditions')}\n"
                    f"Allergies: {patient_details.get('allergies')}\n"
                )
                patient_label = QLabel(patient_info)
                patient_label.setFont(QFont("Arial", 12))

                # Add a button to select the patient
                select_button = QPushButton("View Medical Records")
                select_button.setStyleSheet(self.button_style())
                select_button.clicked.connect(lambda _, addr=patient_address: self.select_patient(addr))


                # Add patient details and button to the layout
                patient_layout.addWidget(patient_label)
                patient_layout.addWidget(select_button)
                patient_widget.setLayout(patient_layout)

                self.patients_page.layout().addWidget(patient_widget)
        except Exception as e:
            print(f"Error fetching patients: {e}")

    def select_patient(self, patient_address):
        self.selected_patient_address = patient_address
        print(f"Selected patient: {self.selected_patient_address}")
        self.show_medical_record()  # Navigate to Medical Records page
        self.selected_patient_label.setText(f"Patient: {self.selected_patient_address}")  # Update label




    def show_medical_record(self):
        """
        Navigate to the Medical Records page and update the selected patient label.
        """
        self.stacked_widget.setCurrentIndex(1)  # Switch to Medical Records page
        if self.selected_patient_address:
            print(f"Showing records for patient: {self.selected_patient_address}")
            self.selected_patient_label.setText(f"Patient: {self.selected_patient_address}")
        else:
            print("No patient selected.")
            self.selected_patient_label.setText("No patient selected.")



    def create_medical_record_page(self):
        medical_record_page = QWidget()
        layout = QVBoxLayout()
        
        # Page Title
        label = QLabel("Medical Records Page")
        label.setFont(QFont("Arial", 18, QFont.Bold))
        layout.addWidget(label)

        # Selected Patient Label
        self.selected_patient_label = QLabel("No patient selected")
        self.selected_patient_label.setFont(QFont("Arial", 14))
        layout.addWidget(self.selected_patient_label)

        # File Upload Button
        self.file_input_button = QPushButton("Upload a File")
        self.file_input_button.setStyleSheet(self.button_style())
        self.file_input_button.clicked.connect(self.upload_file_to_ipfs)
        layout.addWidget(self.file_input_button)

        # File Path Label
        self.file_label = QLabel("No file selected")  # Define the file_label attribute
        self.file_label.setFont(QFont("Arial", 12))
        layout.addWidget(self.file_label)

        # File Upload Status Label
        self.file_status_label = QLabel("")  # Initialize the file status label
        self.file_status_label.setFont(QFont("Arial", 12))
        self.file_status_label.setStyleSheet("color: #FF0000;")  # Red for error messages
        layout.addWidget(self.file_status_label)

        # Display Uploaded Files Section
        self.uploaded_files_groupbox = QGroupBox("Uploaded Files")
        self.uploaded_files_layout = QVBoxLayout()
        self.uploaded_files_groupbox.setLayout(self.uploaded_files_layout)
        layout.addWidget(self.uploaded_files_groupbox)

        # Fetch and display uploaded files for the selected patient
        self.fetch_and_display_patient_files()

        medical_record_page.setLayout(layout)
        return medical_record_page



    def upload_file_to_ipfs(self):
        if not self.selected_patient_address:
            self.file_status_label.setText("No patient selected.")
            return

        file_path, _ = QFileDialog.getOpenFileName(self, "Select a File", "", "All Files (*.*)")
        if file_path:
            try:
                # Upload the file to IPFS
                client = ipfshttpclient.connect("/dns/localhost/tcp/5001/http")
                res = client.add(file_path)
                file_hash = res['Hash']
                file_name = res['Name']
                print(f"File uploaded to IPFS: {file_name} (Hash: {file_hash})")

                # Log the file on the blockchain
                self.log_file_on_blockchain(file_name, file_hash)

                # Update the UI with the new file
                self.update_uploaded_files_display(file_name, file_hash)
                self.fetch_and_display_patient_files()  # Refresh the list of uploaded files

                self.file_status_label.setStyleSheet("color: #00FF00;")  # Green for success
                self.file_status_label.setText(f"File {file_name} uploaded successfully.")
            except Exception as e:
                self.file_status_label.setStyleSheet("color: #FF0000;")
                self.file_status_label.setText(f"Error uploading file: {str(e)}")
                print(f"Error uploading file: {e}")


    def update_uploaded_files_display(self, file_name, file_hash):
        """Update the list of uploaded files in the UI."""
        # Generate the IPFS link
        ipfs_link = f"http://localhost:8080/ipfs/{file_hash}"

        # Create a clickable file link
        file_link = QLabel(f'<a href="{ipfs_link}" style="color: blue;">{file_name}</a>')
        file_link.setFont(QFont("Arial", 12))
        file_link.setOpenExternalLinks(True)  # Enables opening the link in the browser
        self.uploaded_files_layout.addWidget(file_link)

        # Optionally add a timestamp
        timestamp_label = QLabel(f"Uploaded on: {self.blockchain.web3.eth.get_block('latest')['timestamp']}")
        timestamp_label.setFont(QFont("Arial", 10))
        self.uploaded_files_layout.addWidget(timestamp_label)





    def log_file_on_blockchain(self, file_name, file_hash):
        """Log the uploaded file on the blockchain."""
        try:
            # Fetch the doctor contract address
            doctor_contract_address = self.blockchain.get_doctor_contract(self.doctor_address)
            if not doctor_contract_address:
                self.file_status_label.setText("Doctor contract not found.")
                return

            # Log the file on the blockchain
            self.blockchain.upload_file(
                doctor_contract_address=doctor_contract_address,
                patient_address=self.selected_patient_address,
                file_name=file_name,
                file_hash=file_hash,
            )
            print(f"File {file_name} logged on blockchain with hash {file_hash} for patient {self.selected_patient_address}.")
        except Exception as e:
            self.file_status_label.setText(f"Error logging file: {str(e)}")



    def create_patients_page(self):
        """
        Create the Patients Page layout.
        """
        self.patients_page = QWidget()  # Assign to self.patients_page
        layout = QVBoxLayout()

        # Title
        title = QLabel("Patients Who Granted Permission")
        title.setFont(QFont("Arial", 18, QFont.Bold))
        layout.addWidget(title)

        self.patients_page.setLayout(layout)
        return self.patients_page


    def fetch_doctor_information(self):
        """Fetch doctor's name and address from the blockchain."""
        try:
            # Fetch details from the blockchain
            doctor_details = self.blockchain.get_doctor_details(self.doctor_address)
            if doctor_details:
                self.doctor_details = doctor_details
                self.update_doctor_info_label()
            else:
                self.doctor_info_label.setText("No doctor information found.")
        except Exception as e:
            self.doctor_info_label.setText(f"Error: {e}")

    def update_doctor_info_label(self):
        """Update the home page with the doctor's name and address."""
        name = self.doctor_details.get("name", "Unknown")
        address = self.doctor_address
        self.doctor_name_label.setText(f"Dr. {name}")  # Add 'Dr.' before the name
        self.doctor_address_label.setText(f"Address: {address}")


    def button_style(self):
        return """
        QPushButton {
            background-color: #001F3F;
            color: white;
            border: none;
            border-radius: 5px;
            padding: 10px;
            font-size: 16px;
            margin: 10px 0;
        }
        QPushButton:hover {
            background-color: #001F3F;
        }
        """

    def show_home(self):
        self.stacked_widget.setCurrentIndex(0)

    def clear_layout(self, layout):
        """Clear all widgets from a layout."""
        while layout.count():
            item = layout.takeAt(0)
            widget = item.widget()
            if widget is not None:
                widget.deleteLater()



    def view_patient_details(self, patient_address):
        """
        Fetch and display details of a specific patient.
        """
        try:
            patient_contract_address = self.blockchain.get_patient_contract(patient_address)
            patient_details = self.blockchain.get_patient_details(patient_contract_address)

            # Display patient details in a dialog or dedicated page
            details = "\n".join([f"{key.capitalize()}: {value}" for key, value in patient_details.items()])
            print(f"Details for patient {patient_address}:\n{details}")
        except Exception as e:
            print(f"Error fetching details for patient {patient_address}: {e}")

    
    def fetch_and_display_patient_files(self):
        """Fetch and display files uploaded for the selected patient."""
        if not self.selected_patient_address:
            self.file_status_label.setStyleSheet("color: #FF0000;")
            self.file_status_label.setText("No patient selected.")
            return

        try:
            # Fetch the doctor's contract address
            doctor_contract_address = self.blockchain.get_doctor_contract(self.doctor_address)

            if not doctor_contract_address:
                self.file_status_label.setStyleSheet("color: #FF0000;")
                self.file_status_label.setText("Doctor contract not found.")
                return

            # Fetch the list of files for the selected patient
            files = self.blockchain.get_patient_files(doctor_contract_address, self.selected_patient_address)

            # Clear the previous file display
            self.clear_layout(self.uploaded_files_layout)

            # Display the files
            if not files:
                no_files_label = QLabel("No files uploaded for this patient.")
                no_files_label.setFont(QFont("Arial", 12))
                no_files_label.setStyleSheet("color: #FF0000;")
                self.uploaded_files_layout.addWidget(no_files_label)
                return

            for file in files:
                file_name = file["fileName"]
                file_hash = file["fileHash"]
                timestamp = file["timestamp"]

                # Create a clickable file link
                ipfs_link = f"http://localhost:8080/ipfs/{file_hash}"
                file_link = QLabel(f'<a href="{ipfs_link}" style="color: blue;">{file_name}</a>')
                file_link.setFont(QFont("Arial", 12))
                file_link.setOpenExternalLinks(True)

                # Timestamp
                timestamp_label = QLabel(f"Uploaded on: {timestamp}")
                timestamp_label.setFont(QFont("Arial", 10))

                # Add to layout
                self.uploaded_files_layout.addWidget(file_link)
                self.uploaded_files_layout.addWidget(timestamp_label)

        except Exception as e:
            print(f"Error fetching patient files: {e}")
            self.file_status_label.setStyleSheet("color: #FF0000;")
            self.file_status_label.setText(f"Error fetching files: {str(e)}")



if __name__ == "__main__":
    app = QApplication(sys.argv)
    # Replace with a valid doctor Ethereum address
    doctor_address = "0xYourDoctorAddress"
    window = DoctorInterface(doctor_address)
    window.show()
    sys.exit(app.exec_())
