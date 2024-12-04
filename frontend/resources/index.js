// Importer Web3
import Web3 from "web3";

// Charger le fichier JSON de Truffle
import PatientContractJSON from "../../build/contracts/PatientRecords.json";

async function init() {
  // Initialiser Web3
  const web3 = new Web3(Web3.givenProvider || "http://127.0.0.1:7545");

  // Récupérer le réseau utilisé
  const networkId = await web3.eth.net.getId();

  // Obtenir l'ABI et l'adresse dynamiquement
  const abi = PatientContractJSON.abi;
  const address = PatientContractJSON.networks[networkId]?.address;

  if (!address) {
    console.error("Contrat non déployé sur ce réseau.");
    return;
  }

  // Créer une instance du contrat
  const patientContract = new web3.eth.Contract(abi, address);

  console.log("Contrat initialisé :", patientContract);
}

init();
