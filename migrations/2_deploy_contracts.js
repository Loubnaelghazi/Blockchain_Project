const AuditContract = artifacts.require("AuditContract"); //deja compile


module.exports = function (deployer) {
 
  const auditAddress = "0xC29969586160E38DEADA4573c155E7D80069329f";

  // Déployer uniquement le contrat AuditContract
  deployer.deploy(AuditContract, auditAddress);
};
