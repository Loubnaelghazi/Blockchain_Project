from web3 import Web3
import json
import os
import logging
import sys 

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), './')))
from config import GANACHE_URL, MEDICAL_CONTRACT_ADDRESS, AUDIT_CONTRACT_ADDRESS

# Configuration du logger
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Fonction utilitaire pour valider une adresse Ethereum
def is_valid_ethereum_address(address):
    return Web3.is_address(address)

class Blockchain:
    def __init__(self):
        # Connexion à Ganache
        self.web3 = Web3(Web3.HTTPProvider(GANACHE_URL))

        # Vérification de la connexion
        if not self.web3.is_connected():
            raise ConnectionError("Impossible de se connecter à Ganache.")

        self.web3.eth.default_account = self.web3.eth.accounts[0]

        # Charger les informations des contrats
        current_dir = os.path.dirname(__file__)

        medical_file_path = os.path.join(current_dir, "../build/contracts/PatientRecords.json")
        with open(medical_file_path, "r") as file:
            medical_contract_info = json.load(file)
            self.medical_abi = medical_contract_info["abi"]

        audit_file_path = os.path.join(current_dir, "../build/contracts/AuditContract.json")
        with open(audit_file_path, "r") as file:
            audit_contract_info = json.load(file)
            self.audit_abi = audit_contract_info["abi"]

        # Adresses des contrats
        self.medical_contract_address = MEDICAL_CONTRACT_ADDRESS
        self.audit_contract_address = AUDIT_CONTRACT_ADDRESS

        # Instances des contrats
        self.medical_contract = self.web3.eth.contract(address=self.medical_contract_address, abi=self.medical_abi)
        self.audit_contract = self.web3.eth.contract(address=self.audit_contract_address, abi=self.audit_abi)

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

        if role is None:
            raise ValueError("Le rôle (Patient ou Docteur) doit être spécifié.")

        logger.info(f"Enregistrement de l'utilisateur : {name}, rôle : {role}")
        return self.execute_transaction(
            self.audit_contract.functions.registerUser,
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
