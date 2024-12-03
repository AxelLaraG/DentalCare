import sys
from PyQt5 import QtWidgets
from PyQt5.uic import loadUi
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


class MainWindowDentista(QtWidgets.QMainWindow):
    def __init__(self, dentista):
        print(dentista)
        super(MainWindowDentista, self).__init__()
        ui_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "MenuPrincipalDentista.ui")
        loadUi(ui_path, self)

        self.btnLogout.clicked.connect(self.logout)
        self.btnAppointments.clicked.connect(lambda: self.show_window("Citas"))
        self.btnRecords.clicked.connect(lambda: self.show_window("Expedientes"))

    def logout(self):
        # Importar MainApp localmente para evitar importación circular
        from Login.LoginWindow import MainApp

        response = QtWidgets.QMessageBox.question(
            self,
            "Cerrar Sesión",
            "¿Estás seguro de que deseas cerrar sesión?",
            QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No,
            QtWidgets.QMessageBox.No
        )

        if response == QtWidgets.QMessageBox.Yes:
            # Crear y mostrar la ventana de Login
            self.login_window = MainApp()
            self.login_window.show()
            self.close()

    def show_window(self, opc):
        if opc == 'Citas':
            QtWidgets.QMessageBox.information(self, "Opción", "Citas")
        elif opc == 'Expedientes':
            QtWidgets.QMessageBox.information(self, "Opción", "Gestión de expedientes")
