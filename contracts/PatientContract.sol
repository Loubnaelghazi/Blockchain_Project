// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

contract PatientContract {
    struct PersonalInfo {
        string gender;
        string dob;
        string bloodType;
        string phone;
        string addressInfo;
        string notes;
        string medicalConditions;
        string allergies;
        uint256 lastUpdated;
    }

    PersonalInfo public personalInfo;
    address public owner;       // Patient's Ethereum address
    address public auditAddress;

    event PersonalInfoUpdated(uint256 timestamp);

    modifier onlyAudit() {
        require(msg.sender == auditAddress, "Only audit can perform this action");
        _;
    }

    constructor(address _auditAddress) {
        auditAddress = _auditAddress;
    }

    function updatePersonalInfo(
        string memory _gender,
        string memory _dob,
        string memory _bloodType,
        string memory _phone,
        string memory _addressInfo,
        string memory _notes,
        string memory _medicalConditions,
        string memory _allergies
    ) public onlyAudit {
        personalInfo = PersonalInfo(
            _gender,
            _dob,
            _bloodType,
            _phone,
            _addressInfo,
            _notes,
            _medicalConditions,
            _allergies,
            block.timestamp
        );

        emit PersonalInfoUpdated(block.timestamp);
    }

    function getPersonalInfo() public view returns (PersonalInfo memory) {
        return personalInfo;
    }
}
