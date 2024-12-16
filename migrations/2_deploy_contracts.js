const AuditContract = artifacts.require("AuditContract");
const PatientContract = artifacts.require("PatientContract");

module.exports = async function (deployer, network, accounts) {
  // The address to be set as the audit address (can use the first account for simplicity)
  const auditAddress = "0x5D4281e40bEf3E5944144C87095a6E7C8bBD28E6";

  console.log("Deploying AuditContract...");
  await deployer.deploy(AuditContract, auditAddress);
  const auditContractInstance = await AuditContract.deployed();
  console.log(`AuditContract deployed at address: ${auditContractInstance.address}`);

  console.log("Deploying PatientContract (optional)...");

  // Deploy a dummy PatientContract (optional) to test interactions
  await deployer.deploy(PatientContract, auditAddress);
  const patientContractInstance = await PatientContract.deployed();
  console.log(`PatientContract deployed at address: ${patientContractInstance.address}`);

  // Additional logic for testing or initializing contracts can go here
};
