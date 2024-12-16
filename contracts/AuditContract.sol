// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

import "./PatientContract.sol";
import "./DoctorContract.sol";

contract AuditContract {
    enum Role { Patient, Doctor }

    struct User {
        string name;
        string contactInfo;
        Role role;
        bool isRegistered;
        address associatedContract; // Address of the associated PatientContract or DoctorContract
    }

    struct Transaction {
        address doctor;
        uint256 timestamp;
        string details;
    }

    mapping(address => User) public users;
    mapping(address => mapping(address => Transaction[])) public transactionHistory;
    mapping(address => mapping(address => bool)) public patientPermissions;
    address public auditAddress;
    address[] public registeredUsers;

    event UserRegistered(address indexed userAddress, Role role);
    event PatientContractCreated(address indexed userAddress, address patientContract);
    event DoctorContractCreated(address indexed userAddress, address doctorContract);
    event TransactionLogged(address indexed patient, address indexed doctor, uint256 timestamp);

    modifier onlyAudit() {
        require(msg.sender == auditAddress, "Only audit can perform this action");
        _;
    }

    constructor(address _auditAddress) {
        auditAddress = _auditAddress;
    }

    function registerUser(
        address _userAddress,
        string memory _name,
        string memory _contactInfo,
        Role _role
    ) public onlyAudit {
        require(!users[_userAddress].isRegistered, "User already registered");

        address associatedContract = address(0);

        if (_role == Role.Patient) {
            // Deploy a new PatientContract for the patient
            PatientContract patientContract = new PatientContract(auditAddress);
            associatedContract = address(patientContract);
            emit PatientContractCreated(_userAddress, associatedContract);
        } else if (_role == Role.Doctor) {
            // Deploy a new DoctorContract for the doctor
            DoctorContract doctorContract = new DoctorContract(_userAddress, auditAddress);
            associatedContract = address(doctorContract);
            emit DoctorContractCreated(_userAddress, associatedContract);
        }

        users[_userAddress] = User(_name, _contactInfo, _role, true, associatedContract);
        registeredUsers.push(_userAddress);
        emit UserRegistered(_userAddress, _role);
    }

    function updateUser(address _userAddress, string memory _name, string memory _contactInfo) public onlyAudit {
        require(users[_userAddress].isRegistered, "User not registered");
        users[_userAddress].name = _name;
        users[_userAddress].contactInfo = _contactInfo;
    }

    function logTransaction(address _patient, string memory _details) public {
        require(users[_patient].isRegistered, "Patient not registered");
        require(users[msg.sender].role == Role.Doctor, "Only doctors can log transactions");

        transactionHistory[_patient][msg.sender].push(Transaction({
            doctor: msg.sender,
            timestamp: block.timestamp,
            details: _details
        }));

        emit TransactionLogged(_patient, msg.sender, block.timestamp);
    }

    function getTransactionHistory(address _patient, address _doctor) public view returns (Transaction[] memory) {
        require(
            msg.sender == auditAddress || msg.sender == _patient || msg.sender == _doctor,
            "Unauthorized access"
        );
        return transactionHistory[_patient][_doctor];
    }

    function getAssociatedContract(address _userAddress) public view returns (address) {
        require(users[_userAddress].isRegistered, "User not registered");
        return users[_userAddress].associatedContract;
    }

    function getAllUsers() public view returns (address[] memory, string[] memory, Role[] memory) {
        uint256 userCount = registeredUsers.length;

        address[] memory addresses = new address[](userCount);
        string[] memory names = new string[](userCount);
        Role[] memory roles = new Role[](userCount);

        for (uint256 i = 0; i < userCount; i++) {
            address userAddress = registeredUsers[i];
            addresses[i] = userAddress;
            names[i] = users[userAddress].name;
            roles[i] = users[userAddress].role;
        }

        return (addresses, names, roles);
    }

    function grantPermission(address _doctor) public {
        require(users[msg.sender].isRegistered, "Only registered patients can grant permission");
        require(users[_doctor].isRegistered && users[_doctor].role == Role.Doctor, "Invalid doctor");
        patientPermissions[msg.sender][_doctor] = true;
    }

    function getPermittedPatients(address _doctor) public view returns (address[] memory) {
        address[] memory permittedPatients = new address[](registeredUsers.length);
        uint count = 0;
        for (uint i = 0; i < registeredUsers.length; i++) {
            if (patientPermissions[registeredUsers[i]][_doctor]) {
                permittedPatients[count] = registeredUsers[i];
                count++;
            }
        }
        address[] memory result = new address[](count);
        for (uint i = 0; i < count; i++) {
            result[i] = permittedPatients[i];
        }
        return result;
    }

    
}
