
import mysql.connector
from PyQt5.QtWidgets import QApplication, QMainWindow, QMessageBox, QTableWidgetItem
from PyQt5.uic import loadUi
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from Menu.MenuPrincipal import MainWindow


class MainApp(QMainWindow):
    def __init__(self):
        super(MainApp, self).__init__()
        # Obtener la ruta absoluta de Login.ui
        ui_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "Login.ui")
        
        # Cargar la interfaz
        loadUi(ui_path, self)

        self.btn_register_user.clicked.connect(self.register_user)
        self.btn_register_dentist.clicked.connect(self.register_dentist)
        self.btn_login.clicked.connect(self.login)

    def connect_db(self):
        return mysql.connector.connect(
            host="localhost", user="root", password="", database="clinica"
        )

    def register_user(self):
        # Registro de usuarios
        name = self.lineEdit_register_user_name.text()
        lastname = self.lineEdit_register_user_lastname.text()
        age = self.spinBox_register_user_age.value()
        address = self.lineEdit_register_user_address.text()
        email = self.lineEdit_register_user_email.text()
        password = self.lineEdit_register_user_password.text()

        if not name or not lastname or not email or not password:
            QMessageBox.warning(self, "Error", "Todos los campos son obligatorios.")
            return

        try:
            conn = self.connect_db()
            query = """
                INSERT INTO usuarios (nombre, apellido, edad, direccion, email, contrasenia)
                VALUES (%s, %s, %s, %s, %s, %s)
            """
            data = (name, lastname, age, address, email, password)
            cursor = conn.cursor()
            cursor.execute(query, data)
            conn.commit()
            conn.close()
            QMessageBox.information(self, "Éxito", "Usuario registrado exitosamente.")
        except Exception as e:
            QMessageBox.critical(self, "Error", f"No se pudo registrar el usuario.\n{e}")

    def register_dentist(self):
        # Registro de dentistas
        name = self.lineEdit_register_dentist_name.text()
        lastname = self.lineEdit_register_dentist_lastname.text()
        age = self.spinBox_register_dentist_age.value()
        address = self.lineEdit_register_dentist_address.text()
        email = self.lineEdit_register_dentist_email.text()
        password = self.lineEdit_register_dentist_password.text()
        license = self.lineEdit_register_dentist_license.text()

        if not name or not lastname or not email or not password or not license:
            QMessageBox.warning(self, "Error", "Todos los campos son obligatorios.")
            return

        try:
            conn = self.connect_db()
            query = """
                INSERT INTO dentistas (nombre, apellido, edad, direccion, email, contrasenia, licencia)
                VALUES (%s, %s, %s, %s, %s, %s, %s)
            """
            data = (name, lastname, age, address, email, password, license)
            cursor = conn.cursor()
            cursor.execute(query, data)
            conn.commit()
            conn.close()
            QMessageBox.information(self, "Éxito", "Dentista registrado exitosamente.")
        except Exception as e:
            QMessageBox.critical(self, "Error", f"No se pudo registrar el dentista.\n{e}")

    def login(self):
        email = self.lineEdit_login_email.text()
        password = self.lineEdit_login_password.text()

        if not email or not password:
            QMessageBox.warning(self, "Error", "Por favor, llena todos los campos.")
            return

        try:
            conn = self.connect_db()
            query_user = "SELECT nombre FROM usuarios WHERE email=%s AND contrasenia=%s"
            query_dentist = "SELECT nombre FROM dentistas WHERE email=%s AND contrasenia=%s"
            data = (email, password)
            cursor = conn.cursor()

            cursor.execute(query_user, data)
            user = cursor.fetchone()

            if not user:
                cursor.execute(query_dentist, data)
                user = cursor.fetchone()

            conn.close()

            if user:
                QMessageBox.information(self, "Inicio de Sesión", "Inicio de sesión exitoso.")

                # Mostrar la ventana del menú principal
                self.menu_window = MainWindow()
                self.menu_window.show()
                self.close()
            else:
                QMessageBox.warning(self, "Error", "Correo o contraseña incorrectos.")
        except Exception as e:
            QMessageBox.critical(self, "Error", f"No se pudo iniciar sesión.\n{e}")
def main():
    app = QApplication(sys.argv)
    window = MainApp()
    window.show()
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()
