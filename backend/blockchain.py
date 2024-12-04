from web3 import Web3
import json

class Blockchain:
    def __init__(self):
        # Connexion à Ganache (localhost)
        self.web3 = Web3(Web3.HTTPProvider("http://127.0.0.1:7545"))
        
        # Vérification de la connexion
        if not self.web3.is_connected():
            raise ConnectionError("Impossible de se connecter à Ganache.")
        
        self.web3.eth.default_account = self.web3.eth.accounts[0]

        with open("../compiled_contracts/contractPatient.json", "r") as file:
            contract_info = json.load(file)
            self.abi = contract_info["contracts"]["contractPatient.sol"]["PatientRecords"]["abi"]
        
        self.contract_address = "0xA67aD8BfB9FBC17BD2931575804f4391Eeec31C3"
        self.contract = self.web3.eth.contract(address=self.contract_address, abi=self.abi)

    def register_patient(self, name):
        try:
            print(f"Envoi de la transaction pour enregistrer le patient : {name}")
            tx_hash = self.contract.functions.registerPatient(name).transact()
            print(f"Transaction envoyée. Hash : {tx_hash}")
            tx_receipt = self.web3.eth.wait_for_transaction_receipt(tx_hash)
            print(f"Transaction confirmée dans le bloc : {tx_receipt['blockNumber']}")
            return tx_receipt
        except Exception as e:
            print(f"Erreur : {e}")
            return None

    def add_medical_record(self, ipfs_hash, file_name):
        try:
            print(f"Ajout du dossier médical pour {file_name} avec IPFS Hash {ipfs_hash}")
            tx_hash = self.contract.functions.addMedicalRecord(ipfs_hash, file_name).transact()
            print(f"Transaction envoyée. Hash : {tx_hash}")
            tx_receipt = self.web3.eth.wait_for_transaction_receipt(tx_hash)
            print(f"Transaction confirmée dans le bloc : {tx_receipt['blockNumber']}")
            return tx_receipt
        except Exception as e:
            print(f"Erreur : {e}")
            return None

    def get_medical_records(self):
        try:
            records = self.contract.functions.getMedicalRecords().call()
            return records
        except Exception as e:
            print(f"Erreur : {e}")
            return []
