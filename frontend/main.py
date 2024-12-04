from PyQt5.QtWidgets import QMainWindow, QApplication, QPushButton, QFileDialog
from backend.blockchain import Blockchain
from backend.ipfs import IPFSClient

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        # Initialiser les composants de la fenêtre
        self.blockchain = Blockchain()
        self.ipfs = IPFSClient()

        # Initialiser le bouton upload
        self.upload_button = QPushButton("Upload", self)
        self.upload_button.setGeometry(100, 100, 100, 30)  # Définir la position et la taille du bouton

        # Connecter le bouton à la méthode upload_file
        self.upload_button.clicked.connect(self.upload_file)

    def upload_file(self):
        file_path = self.select_file()
        if file_path:
            ipfs_hash = self.ipfs.upload_file(file_path)
            self.blockchain.add_medical_record(ipfs_hash, file_path.split("/")[-1])
            print(f"Fichier ajouté avec succès : {ipfs_hash}")

    def select_file(self):
        # Ouvrir une boîte de dialogue pour sélectionner un fichier
        file_dialog = QFileDialog(self)
        file_dialog.setFileMode(QFileDialog.ExistingFiles)
        file_dialog.setNameFilter("All Files (*)")
        file_dialog.setViewMode(QFileDialog.List)
        
        if file_dialog.exec_():
            selected_files = file_dialog.selectedFiles()
            return selected_files[0]  # Retourner le premier fichier sélectionné
        return None


