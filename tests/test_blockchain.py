

import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../')))

import pytest
from backend.blockchain import Blockchain



def test_register_patient():
    blockchain = Blockchain()
    receipt = blockchain.register_patient("John Doe")
    assert receipt is not None  # Vérifie que la transaction a été confirmee
    assert receipt['status'] == 1 

def test_add_medical_record():
    blockchain = Blockchain()
    ipfs_hash = "QmHashExample"
    file_name = "fichier.pdf"
    receipt = blockchain.add_medical_record(ipfs_hash, file_name)
    assert receipt is not None  # Vérifie que la transaction a été confirmée
    assert receipt['status'] == 1  # Vérifie que le statut de la transaction est "successful"