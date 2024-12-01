import sys
from PyQt5 import QtWidgets, uic
from PyQt5.uic import loadUi
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from Usuarios.CrudDentista import CrudWindowDentists
from Usuarios.CrudUser import CrudWindowUser


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

    def logout(self):
        # Acción del botón "Cerrar Sesión"
        QtWidgets.QMessageBox.information(self, "Cerrar Sesión", "Has cerrado sesión.")
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
            # Abrir la ventana CrudWindowDentists
            QtWidgets.QMessageBox.information(self, "Opción ","Citas")
        elif opc == 'Expedientes':
            # Abrir la ventana CrudWindowDentists
            QtWidgets.QMessageBox.information(self, "Opción ","Gestión de expedientes")

def main():
    app = QtWidgets.QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()
