from PyQt5.QtWidgets import QApplication
from frontend.main import AuditInterface

if __name__ == "__main__":
    app = QApplication([])
    window = AuditInterface()
    window.show()
    app.exec_()

