import sys
from PyQt5 import QtWidgets, uic
from PyQt5.uic import loadUi
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from Usuarios.CrudDentista import CrudWindowDentists
from Usuarios.CrudUser import CrudWindowUser
from Pacientes.PacientesWindow import PacientesCRUD
from Citas.CitasWindow import SemanaApp
from Expedientes.Funciones import MainWindow as ExpedientesWindow


class MainWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        # Obtener la ruta absoluta de Login.ui
        ui_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "MenuPrincipal.ui")
        
        # Cargar la interfaz
        loadUi(ui_path, self)

        # Conectar señales (opcional)
        self.btnLogout.clicked.connect(self.logout)
        self.btnUsers.clicked.connect(lambda: self.show_window("Gestión de Usuarios"))
        self.btnDentists.clicked.connect(lambda: self.show_window("Gestión de Dentistas"))
        self.btnAppointments.clicked.connect(lambda: self.show_window("Citas"))
        self.btnRecords.clicked.connect(lambda: self.show_window("Expedientes"))
        self.btnRecords_2.clicked.connect(lambda: self.show_window("Pacientes"))

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
        # Mostrar un mensaje en un cuadro de diálogo
   
        if opc == 'Gestión de Usuarios':
            # Abrir la ventana CrudWindowUser
            self.crud_user_window = CrudWindowUser()  # Instancia de la ventana CRUD
            self.crud_user_window.show()  # Mostrar la ventana
        
        elif opc == 'Gestión de Dentistas':
            # Abrir la ventana CrudWindowDentists
            self.crud_dentists_window = CrudWindowDentists()  # Instancia de la ventana CRUD
            self.crud_dentists_window.show()  # Mostrar la ventana
        elif opc == 'Citas':
            self.crud_citas_window = SemanaApp()
            self.crud_citas_window.show()
        elif opc == 'Expedientes':
            self.crud_expedientes_window = ExpedientesWindow()
            self.crud_expedientes_window.show()
        elif opc == 'Pacientes':
            self.crud_pacientes_window = PacientesCRUD()
            self.crud_pacientes_window.show()

def main():
    app = QtWidgets.QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()
