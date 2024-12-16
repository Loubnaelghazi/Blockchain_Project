const AuditContract = artifacts.require("AuditContract");
const PatientContract = artifacts.require("PatientContract");

module.exports = async function (deployer, network, accounts) {
  
  const auditAddress = "0x5D4281e40bEf3E5944144C87095a6E7C8bBD28E6";

  console.log("Deploying AuditContract...");
  await deployer.deploy(AuditContract, auditAddress);
  const auditContractInstance = await AuditContract.deployed();
  console.log(`AuditContract deployed at address: ${auditContractInstance.address}`);

  console.log("Deploying PatientContract (optional)...");


  await deployer.deploy(PatientContract, auditAddress);
  const patientContractInstance = await PatientContract.deployed();
  console.log(`PatientContract deployed at address: ${patientContractInstance.address}`);

  
};
