from solcx import  install_solc, compile_standard
from web3 import Web3
import json

install_solc('0.8.0')
# Charger le contrat Solidity
with open("../contracts/contractPatient.sol", "r") as file:
    contract_source_code = file.read()

# Compiler le contrat
compiled_sol = compile_standard(
    {
        "language": "Solidity",
        "sources": {"contractPatient.sol": {"content": contract_source_code}},
        "settings": {"outputSelection": {"*": {"*": ["abi", "evm.bytecode"]}}},
    },
    solc_version="0.8.0",
)
compiled_file = "../compiled_contracts/contractPatient.json"
with open(compiled_file, "w") as file:
    json.dump(compiled_sol, file)
# Enregistrer l'ABI et le bytecode
abi = compiled_sol["contracts"]["contractPatient.sol"]["PatientRecords"]["abi"]
bytecode = compiled_sol["contracts"]["contractPatient.sol"]["PatientRecords"]["evm"]["bytecode"]["object"]

# Connexion à Ganache
web3 = Web3(Web3.HTTPProvider("http://127.0.0.1:7545"))
web3.eth.default_account = web3.eth.accounts[0]

# Déployer le contrat
MedicalRecords = web3.eth.contract(abi=abi, bytecode=bytecode)
tx_hash = MedicalRecords.constructor().transact()
tx_receipt = web3.eth.wait_for_transaction_receipt(tx_hash)

contract_address = tx_receipt.contractAddress
print(f"Contrat déployé à : {contract_address}")

