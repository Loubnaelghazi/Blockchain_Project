// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

contract AuditContract {
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

    event UserRegistered(address indexed userAddress, Role role);
    event TransactionLogged(address indexed patient, address indexed doctor, uint256 timestamp);

    modifier onlyAudit() {
        require(msg.sender == auditAddress, "Only audit can perform this action");
        _;
    }

    constructor(address _auditAddress) {
        auditAddress = _auditAddress;
    }

    function registerUser(address _userAddress, string memory _name, string memory _contactInfo, Role _role) public onlyAudit {
        require(!users[_userAddress].isRegistered, "User already registered");
        users[_userAddress] = User(_name, _contactInfo, _role, true);
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
}
