// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

contract MedicalBlockchain {
    enum Role {Patient, Doctor}
    mapping(address => User) public users;
    mapping(address => mapping(address => Transaction[])) public transactionHistory;
    address public auditAddress;

    struct User {
        string name;
        string contactInfo;
        Role role;
        bool isRegistered;
    }

    struct Transaction {
        address doctor;
        uint256 timestamp;
        string details;
    }

    modifier onlyAudit() {
        require(msg.sender == auditAddress, "Only audit can perform this action");
        _;
    }

    // Constructor: Set the audit address
    constructor(address _auditAddress) {
        auditAddress = _auditAddress;
    }

    // Function to register a new user (either a patient or doctor)
    function registerUser(address _userAddress, string memory _name, string memory _contactInfo, uint8 _role) public onlyAudit {
        require(!users[_userAddress].isRegistered, "User already registered");

        Role userRole;
        if (_role == 0) {
            userRole = Role.Patient;
        } else if (_role == 1) {
            userRole = Role.Doctor;
        } else {
            revert("Invalid role");
        }

        users[_userAddress] = User({
            name: _name,
            contactInfo: _contactInfo,
            role: userRole,
            isRegistered: true
        });
    }

    // Function to log a transaction between a patient and a doctor
    function logTransaction(address _patient, string memory _details) public {
        require(users[_patient].isRegistered, "Patient not registered");
        require(users[msg.sender].role == Role.Doctor, "Only doctors can log transactions");

        Transaction memory newTransaction = Transaction({
            doctor: msg.sender,
            timestamp: block.timestamp,
            details: _details
        });

        transactionHistory[_patient][msg.sender].push(newTransaction);
    }

    // Function to retrieve transaction history for a patient
    function getTransactionHistory(address _patient, address _doctor) public view returns (Transaction[] memory) {
        require(msg.sender == auditAddress, "Only audit can view transaction history");
        return transactionHistory[_patient][_doctor];
    }
}
