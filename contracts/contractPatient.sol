// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

contract PatientRecords {

    // Définir la structure pour un dossier médical
    struct Record {
        string ipfsHash;
        string fileName;
        uint256 timestamp;
    }

    // Définir la structure pour un patient
    struct Patient {
        string name;
        address walletAddress;
        uint256 recordCount; // Compteur pour suivre le nombre de dossiers médicaux
    }

    // Mappage d'adresse à Patient
    mapping(address => Patient) private patients;

    // Mappage d'adresse à mappage d'index de dossier à Record
    mapping(address => mapping(uint256 => Record)) private patientRecords;
    
    // Liste des adresses des patients
    address[] private patientAddresses;

    // Enregistrer un patient
    function registerPatient(string memory _name) public {
        require(bytes(_name).length > 0, "Le nom est obligatoire");
        require(bytes(patients[msg.sender].name).length == 0, "Patient deja enregistre");

        patients[msg.sender] = Patient({
            name: _name,
            walletAddress: msg.sender,
            recordCount: 0 // Initialiser le compteur de dossiers à 0
        });

        patientAddresses.push(msg.sender);
    }

    // Ajouter un dossier médical pour un patient
    function addMedicalRecord(string memory _ipfsHash, string memory _fileName) public {
        require(bytes(_ipfsHash).length > 0, "Le hash IPFS est obligatoire");
        require(bytes(_fileName).length > 0, "Le nom du fichier est obligatoire");
        require(bytes(patients[msg.sender].name).length > 0, "Patient non enregistre");

        uint256 recordIndex = patients[msg.sender].recordCount;

        // Créer un nouveau dossier médical
        Record memory newRecord = Record({
            ipfsHash: _ipfsHash,
            fileName: _fileName,
            timestamp: block.timestamp
        });

        // Sauvegarder le dossier médical dans le mappage
        patientRecords[msg.sender][recordIndex] = newRecord;

        // Mettre à jour le compteur de dossiers
        patients[msg.sender].recordCount++;
    }

    // Récupérer les dossiers médicaux d'un patient
    function getMedicalRecords() public view returns (Record[] memory) {
        require(bytes(patients[msg.sender].name).length > 0, "Patient non enregistre");

        uint256 recordCount = patients[msg.sender].recordCount;
        Record[] memory records = new Record[](recordCount);

        for (uint256 i = 0; i < recordCount; i++) {
            records[i] = patientRecords[msg.sender][i];
        }

        return records;
    }

    // Récupérer les informations d'un patient
    function getPatientInfo() public view returns (string memory, address, uint256) {
        require(bytes(patients[msg.sender].name).length > 0, "Patient non enregistre");
        return (
            patients[msg.sender].name,
            patients[msg.sender].walletAddress,
            patients[msg.sender].recordCount
        );
    }

    // Liste des adresses des patients (administrateurs seulement)
    function getAllPatients() public view returns (address[] memory) {
        return patientAddresses;
    }
}