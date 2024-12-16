from web3 import Web3
import json
import os
import logging
import sys 

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), './')))
from config import GANACHE_URL, MEDICAL_CONTRACT_ADDRESS, AUDIT_CONTRACT_ADDRESS, PATIENT_RECORDS_ADRESS

# Configuration du logger
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Fonction utilitaire pour valider une adresse Ethereum
def is_valid_ethereum_address(address):
    return Web3.is_address(address)

class Blockchain:
    def __init__(self, doctor_address=None):
        # Connexion à Ganache
        self.web3 = Web3(Web3.HTTPProvider(GANACHE_URL))

        # Vérification de la connexion
        if not self.web3.is_connected():
            raise ConnectionError("Impossible de se connecter à Ganache.")

        self.web3.eth.default_account = self.web3.eth.accounts[0]

        # Store doctor_address if provided
        self.doctor_address = doctor_address

        # Charger les informations des contrats
        current_dir = os.path.dirname(__file__)

        medical_file_path = os.path.join(current_dir, "../build/contracts/AuditContract.json")
        with open(medical_file_path, "r") as file:
            medical_contract_info = json.load(file)
            self.medical_abi = medical_contract_info["abi"]

        audit_file_path = os.path.join(current_dir, "../build/contracts/AuditContract.json")
        with open(audit_file_path, "r") as file:
            audit_contract_info = json.load(file)
            self.audit_abi = audit_contract_info["abi"]
        
        patient_file_path = os.path.join(current_dir, "../build/contracts/PatientContract.json")
        with open(patient_file_path, "r") as file:
            patient_contract_info = json.load(file)
            self.patient_abi = patient_contract_info["abi"]

        doctor_file_path = os.path.join(current_dir, "../build/contracts/DoctorContract.json")
        with open(doctor_file_path, "r") as file:
            doctor_contract_info = json.load(file)
            self.doctor_abi = doctor_contract_info["abi"]

        # Adresses des contrats
        self.medical_contract_address = MEDICAL_CONTRACT_ADDRESS
        self.audit_contract_address = AUDIT_CONTRACT_ADDRESS
        self.patient_contract_address = PATIENT_RECORDS_ADRESS

        # Instances des contrats
        self.medical_contract = self.web3.eth.contract(address=self.medical_contract_address, abi=self.medical_abi)
        self.audit_contract = self.web3.eth.contract(address=self.audit_contract_address, abi=self.audit_abi)
        self.patient_contract = self.web3.eth.contract(address=self.patient_contract_address, abi=self.patient_abi)

    def execute_transaction(self, function, *args):
        """
        Méthode générique pour exécuter une transaction et attendre la confirmation.
        """
        try:
            tx_hash = function(*args).transact()
            logger.info(f"Transaction envoyée. Hash : {tx_hash.hex()}")
            tx_receipt = self.web3.eth.wait_for_transaction_receipt(tx_hash)
            logger.info(f"Transaction confirmée dans le bloc : {tx_receipt['blockNumber']}")
            return tx_receipt
        except Exception as e:
            logger.error(f"Erreur lors de l'exécution de la transaction : {e}")
            return None

    def register_user(self, user_address, name, contact_info="", role=None):
        """
        Enregistre un utilisateur. Le rôle est défini automatiquement si non fourni.
        """
        if not is_valid_ethereum_address(user_address):
            raise ValueError(f"Adresse Ethereum invalide : {user_address}")

        if role is None or role not in [0, 1]:
            raise ValueError("Le rôle (0 pour Patient, 1 pour Docteur) doit être spécifié.")

        logger.info(f"Enregistrement de l'utilisateur : {name}, rôle : {role}")
        return self.execute_transaction(
            self.medical_contract.functions.registerUser,
            user_address, name, contact_info, role
    )


    def log_transaction(self, patient_address, details):
        """
        Enregistre une transaction entre un médecin et un patient via MedicalBlockchain.
        """
        if not is_valid_ethereum_address(patient_address):
            raise ValueError(f"Adresse Ethereum invalide : {patient_address}")

        logger.info(f"Enregistrement d'une transaction pour le patient : {patient_address}")
        return self.execute_transaction(
            self.medical_contract.functions.logTransaction,
            patient_address, details
        )

    def get_transaction_history(self, patient_address, doctor_address):
        """
        Récupère l'historique des transactions entre un patient et un médecin.
        """
        try:
            logger.info(f"Récupération de l'historique pour le patient {patient_address} et le médecin {doctor_address}")
            history = self.medical_contract.functions.getTransactionHistory(patient_address, doctor_address).call()
            return history
        except Exception as e:
            logger.error(f"Erreur lors de la récupération de l'historique : {e}")
            return []

    def is_audit(self):
        """
        Vérifie si l'utilisateur actuel est défini comme audit dans AuditContract.
        """
        try:
            audit_address = self.audit_contract.functions.auditAddress().call()
            is_audit = self.web3.eth.default_account == audit_address
            logger.info(f"Utilisateur actuel est audit : {is_audit}")
            return is_audit
        except Exception as e:
            logger.error(f"Erreur lors de la vérification de l'audit : {e}")
            return False

    def get_patients(self):
        """
        Fetches the list of patients from the AuditContract.
        """
        try:
            # Call to get all users
            all_users = self.medical_contract.functions.getAllUsers().call()  # Use audit_contract here
            logger.info(f"Raw output from getAllUsers: {all_users}")
            
            if not all_users:
                logger.warning("No users found.")
                return []

            addresses, names, roles = all_users

            # Filter users based on role 0 (Patient)
            patients = [
                {"address": addresses[i], "name": names[i], "role": roles[i]}
                for i in range(len(addresses)) if roles[i] == 0  # Role 0 is Patient
            ]
            logger.info(f"Fetched {len(patients)} patients.")
            return patients
        except Exception as e:
            logger.error(f"Error fetching patients: {e}")
            return []  # Return an empty list if there's an issue

    def get_doctors(self):
        """
        Fetches the list of doctors from the AuditContract.
        """
        try:
            # Call to get all users
            all_users = self.medical_contract.functions.getAllUsers().call()  # Use audit_contract here
            logger.info(f"Raw output from getAllUsers: {all_users}")
            
            if not all_users:
                logger.warning("No users found.")
                return []

            addresses, names, roles = all_users

            # Filter users based on role 1 (Doctor)
            doctors = [
                {"address": addresses[i], "name": names[i], "role": roles[i]}
                for i in range(len(addresses)) if roles[i] == 1  # Role 1 is Doctor
            ]
            logger.info(f"Fetched {len(doctors)} doctors.")
            return doctors
        except Exception as e:
            logger.error(f"Error fetching doctors: {e}")
            return []  # Return an empty list if there's an issue

    def get_permitted_patients(self, patient_address):
        try:
            # Call the blockchain to fetch permitted doctors
            permitted_doctors = self.medical_contract.functions.getPermittedPatients(patient_address).call()
            print(f"Permitted doctors for patient {patient_address}: {permitted_doctors}")
            return permitted_doctors
        except Exception as e:
            print(f"Error fetching permitted doctors: {e}")
            return []


    def get_patient_contract(self, patient_address):
        """Fetch the PatientContract address for a given patient."""
        try:
            return self.medical_contract.functions.getAssociatedContract(patient_address).call()
        except Exception as e:
            print(f"Error fetching patient contract: {e}")
            return None

    def get_patient_details(self, patient_contract_address):
        """Fetch personal details of a patient from their PatientContract."""
        try:
            contract = self.web3.eth.contract(address=patient_contract_address, abi=self.patient_abi)
            personal_info = contract.functions.getPersonalInfo().call()
            return {
                "gender": personal_info[0],
                "dob": personal_info[1],
                "bloodType": personal_info[2],
                "phone": personal_info[3],
                "addressInfo": personal_info[4],
                "notes": personal_info[5],
                "medicalConditions": personal_info[6],
                "allergies": personal_info[7],
                "lastUpdated": personal_info[8],
            }
        except Exception as e:
            print(f"Error fetching patient details: {e}")
            return {}



    def update_patient_details(self, patient_contract_address, details):
        """
        Update patient details in the PatientContract.
        """
        try:
            contract = self.web3.eth.contract(address=patient_contract_address, abi=self.patient_abi)
            self.execute_transaction(
                contract.functions.updatePersonalInfo,
                details["gender"],
                details["date of birth"],
                details["bloodType"],
                details["phone"],
                details["addressInfo"],
                details["notes"],
                details["medicalConditions"],
                details["allergies"]
            )
            logger.info(f"Updated patient details in contract: {patient_contract_address}")
        except Exception as e:
            logger.error(f"Error updating patient details: {e}")

    def get_doctor_details(self, doctor_address):
        """
        Fetches the details of a doctor from the blockchain.
        :param doctor_address: Ethereum address of the doctor.
        :return: A dictionary containing the doctor's name, contact info, and role.
        """
        try:
            # Validate the Ethereum address
            if not is_valid_ethereum_address(doctor_address):
                raise ValueError(f"Invalid Ethereum address: {doctor_address}")

            # Fetch doctor data from the contract
            doctor_data = self.medical_contract.functions.users(doctor_address).call()
            is_registered = doctor_data[3]  # Boolean indicating registration status
            role = doctor_data[2]  # Enum indicating the role (0 = Patient, 1 = Doctor)

            # Ensure the user is a registered doctor
            if not is_registered or role != 1:
                raise ValueError(f"Address {doctor_address} is not registered as a doctor.")

            # Extract details (adjust indices as per your smart contract's `User` struct)
            doctor_details = {
                "name": doctor_data[0],  # Assuming 'name' is the first field in User struct
                "contactInfo": doctor_data[1],  # Assuming 'contactInfo' is the second field
                "role": "Doctor",  # Hardcoded as we confirmed the role
            }
            return doctor_details

        except Exception as e:
            logger.error(f"Error fetching doctor details: {e}")
            return None
        
    def grant_permission(self, doctor_address):
        """Grant permission to a doctor."""
        try:
            # Log default account
            print(f"Executing grantPermission with default_account: {self.web3.eth.default_account}")

            return self.execute_transaction(
                self.medical_contract.functions.grantPermission,
                doctor_address
            )
        except Exception as e:
            print(f"Error in grant_permission: {e}")
            raise
    
    def grant_permission_to_doctor(self, patient_address, doctor_address):
        try:
            self.blockchain.grant_permission(doctor_address)
            print(f"Permission granted for doctor {doctor_address} by patient {patient_address}")
        except Exception as e:
            print(f"Error granting permission: {e}")



    def is_registered_patient(self, patient_address):
        """Check if a patient is registered."""
        try:
            user_data = self.medical_contract.functions.users(patient_address).call()
            is_registered = user_data[3] and user_data[2] == 0  # isRegistered and Role.Patient
            print(f"Patient {patient_address} registered: {is_registered}")
            return is_registered
        except Exception as e:
            print(f"Error checking patient registration: {e}")
            return False
        
    def upload_file(self, doctor_contract_address, patient_address, file_name, file_hash):
        """
        Upload a file for a specific patient via the DoctorContract.
        """
        try:
            # Ensure the doctor's Ethereum address is used as the sender
            self.web3.eth.default_account = self.doctor_address
            print(f"Default account set to: {self.web3.eth.default_account}")
            
            # Interact with the DoctorContract
            doctor_contract = self.web3.eth.contract(address=doctor_contract_address, abi=self.doctor_abi)
            return self.execute_transaction(
                doctor_contract.functions.uploadFile,
                patient_address, file_name, file_hash
            )
        except Exception as e:
            logger.error(f"Error uploading file for patient: {e}")
            return None


    def get_doctor_contract(self, doctor_address):
        """
        Fetch the DoctorContract address for the given doctor.
        """
        try:
            doctor_contract_address = self.medical_contract.functions.getAssociatedContract(doctor_address).call()
            if not doctor_contract_address or doctor_contract_address == "0x0000000000000000000000000000000000000000":
                raise ValueError("No DoctorContract associated with this doctor.")
            return doctor_contract_address
        except Exception as e:
            logger.error(f"Error fetching DoctorContract address: {e}")
            return None

    def get_patient_files(self, doctor_contract_address, patient_address):
        """Fetch files uploaded for a patient by the doctor."""
        try:
            contract = self.web3.eth.contract(address=doctor_contract_address, abi=self.doctor_abi)
            files = contract.functions.getPatientFiles(patient_address).call()
            return [
                {
                    "fileName": file[0],
                    "fileHash": file[1],
                    "timestamp": file[2],
                }
                for file in files
            ]
        except Exception as e:
            print(f"Error fetching patient files: {e}")
            return []

    def get_all_transactions(self):
        try:
            transactions = self.medical_contract.functions.getAllTransactions().call()
            patients, doctors, timestamps, details = transactions

            return [
                {
                    "patient": patients[i],
                    "doctor": doctors[i],
                    "timestamp": timestamps[i],
                    "details": details[i],
                }
                for i in range(len(patients))
            ]
        except Exception as e:
            logger.error(f"Error fetching transactions: {e}")
            return []


