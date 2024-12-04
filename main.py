from PyQt5.QtWidgets import QApplication
from frontend.main import BlockchainApp

if __name__ == "__main__":
    import sys
    app = QApplication(sys.argv)
    window = BlockchainApp()
    window.show()
    sys.exit(app.exec_())

