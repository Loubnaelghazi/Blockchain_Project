from web3 import Web3
import json
import os

# Connect to Ganache
ganache_url = "http://127.0.0.1:7545"
web3 = Web3(Web3.HTTPProvider(ganache_url))

# Load ABI
current_dir = os.path.dirname(os.path.abspath(__file__))
audit_file_path = os.path.join(current_dir, r"C:\Users\IMANE\Desktop\Blockchain\Blockchain_Project\build\contracts\AuditContract.json")

with open(audit_file_path, "r") as file:
    audit_contract_info = json.load(file)
    contract_abi = audit_contract_info["abi"]

# Contract address
contract_address = "0xF8E01f78B71dE99bE54B887b494D36BD65677281"

# Load the contract
contract = web3.eth.contract(address=contract_address, abi=contract_abi)

# Verify audit address
audit_address = contract.functions.auditAddress().call()
print(f"Audit address: {audit_address}")

# Register a user
user_address = "0xD237AC93F470BA15B6aFF71a57F806AE9a3A021c"
web3.eth.default_account = audit_address  # Ensure this matches the auditAddress
tx_hash = contract.functions.registerUser(
    user_address, "Test User", "Contact Info", 0
).transact()
receipt = web3.eth.wait_for_transaction_receipt(tx_hash)
print("Transaction receipt:", receipt)

# Check user data
user_data = contract.functions.users(user_address).call()
print("Données utilisateur enregistrées :", user_data)