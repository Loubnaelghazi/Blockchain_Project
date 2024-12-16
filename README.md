# Medical Records Blockchain Project

## Table of Contents

1. [Introduction](#introduction)
2. [Problem Statement](#problem-statement)
3. [Project Objectives](#project-objectives)
4. [System Design](#system-design)
5. [Technologies Used](#technologies-used)
6. [Setup and Installation](#setup-and-installation)

---

## Introduction

Managing medical records securely and efficiently is a critical challenge in the healthcare sector. Traditional centralized systems are prone to cyberattacks, human errors, and unauthorized access. This project leverages blockchain technology to provide a decentralized, transparent, and secure solution for managing medical records.

## Problem Statement

Healthcare data management faces several issues:

- Vulnerability to cyberattacks
- Lack of data traceability
- Inefficient data access and sharing mechanisms
- Human error risks

This project aims to address these problems by using Ethereum blockchain, smart contracts, and distributed storage systems.

## Project Objectives

1. **Secure Medical Data**: Use blockchain immutability and decentralized storage to protect sensitive information.
2. **Access Control**: Implement smart contracts for precise permission management.
3. **Data Sharing**: Facilitate secure and transparent sharing between patients and healthcare providers.
4. **Traceability**: Ensure all interactions are logged for audit and transparency.
5. **User-Friendly Interface**: Provide an intuitive interface for all users.

## System Design

### Architecture Overview

The system consists of:

1. **Blockchain**: Ethereum network for decentralized transaction management.
2. **Smart Contracts**:
   - `AuditContract`: Manages user registration and permissions.
   - `PatientContract`: Stores patient information and associated records.
   - `DoctorContract`: Allows doctors to upload and manage patient files.
3. **Distributed Storage**: IPFS for storing medical files securely.
4. **Frontend**: PyQt-based interface for user interactions.

### Key Interactions

- Patients control access to their records.
- Doctors upload files and manage permissions via smart contracts.
- Auditors verify transactions and interactions.

## Technologies Used

1. **Blockchain**:
   - Ethereum
   - Solidity (smart contract development)
2. **Distributed Storage**:
   - IPFS
3. **Frontend**:
   - PyQt
   - Web3.py for blockchain interactions
4. **Development Tools**:
   - Truffle
   - Ganache (local Ethereum blockchain for testing)

## Setup and Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/Loubnaelghazi/Blockchain_Project
   cd medical-records-blockchain
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Start Ganache for a local Ethereum blockchain:
   ```bash
   ganache-cli
   ```

4. Deploy smart contracts using Truffle:
   ```bash
   truffle migrate --network development
   ```

5. Launch the PyQt interface:
   ```bash
   python app.py
   ```

## Usage

1. **Login**: Patients, doctors, and auditors authenticate using Ethereum wallets.
2. **Manage Permissions**:
   - Patients grant or revoke access to doctors.
   - Doctors access and upload medical records via IPFS.
3. **Audit Logs**: Auditors view interaction histories stored on the blockchain.





