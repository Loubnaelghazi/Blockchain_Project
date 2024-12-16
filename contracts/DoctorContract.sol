// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

contract DoctorContract {
    address public doctorAddress;
    address public auditAddress;

    struct Patient {
        address patientAddress;
        address patientContract;
    }

    struct File {
        string fileName;
        string fileHash;
        uint256 timestamp;
    }


    mapping(address => bool) private authorizedPatients; // Track authorized patients
    mapping(address => File[]) private patientFiles; // Track files uploaded for each patient
    Patient[] public patientList;

    event PermissionGranted(address indexed patientAddress, address indexed patientContract);
    event FileUploaded(address indexed patientAddress, string fileName, string fileHash);

    modifier onlyDoctor() {
        require(msg.sender == doctorAddress, "Only the doctor can perform this action");
        _;
    }

    modifier onlyAudit() {
        require(msg.sender == auditAddress, "Only audit can perform this action");
        _;
    }

    constructor(address _doctorAddress, address _auditAddress) {
        doctorAddress = _doctorAddress;
        auditAddress = _auditAddress;
    }

    function addPatient(address _patientAddress, address _patientContract) external onlyAudit {
        require(!authorizedPatients[_patientAddress], "Patient already authorized");
        authorizedPatients[_patientAddress] = true;

        patientList.push(Patient(_patientAddress, _patientContract));
        emit PermissionGranted(_patientAddress, _patientContract);
    }

   function uploadFile(address _patientAddress, string memory _fileName, string memory _fileHash) external onlyDoctor {
        require(_patientAddress != address(0), "Invalid patient address");
        patientFiles[_patientAddress].push(File({
            fileName: _fileName,
            fileHash: _fileHash,
            timestamp: block.timestamp
        }));
        emit FileUploaded(_patientAddress, _fileName, _fileHash);
    }



    function getPatientFiles(address _patientAddress) external view returns (File[] memory) {
        // Remove the access control restriction to allow all users access
        return patientFiles[_patientAddress];
    }




    function getAuthorizedPatients() external view returns (address[] memory) {
        address[] memory addresses = new address[](patientList.length);
        for (uint256 i = 0; i < patientList.length; i++) {
            addresses[i] = patientList[i].patientAddress;
        }
        return addresses;
    }
}
