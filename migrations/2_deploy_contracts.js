const PatientRecords = artifacts.require("PatientRecords");

module.exports = function (deployer) {
  deployer.deploy(PatientRecords);
};
