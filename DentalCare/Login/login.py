import sys
import mysql.connector
from PyQt5.QtWidgets import QApplication, QMainWindow, QMessageBox, QTableWidgetItem
from PyQt5.uic import loadUi

class MainApp(QMainWindow):
    def __init__(self):
        super(MainApp, self).__init__()
        loadUi("Login.ui", self)

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
                self.menu_window = MenuWindow()
                self.menu_window.show()
                self.close()
            else:
                QMessageBox.warning(self, "Error", "Correo o contraseña incorrectos.")
        except Exception as e:
            QMessageBox.critical(self, "Error", f"No se pudo iniciar sesión.\n{e}")


class MenuWindow(QMainWindow):
    def __init__(self):
        super(MenuWindow, self).__init__()
        loadUi("Menu.ui", self)

        self.Usuarios.clicked.connect(self.show_users)
        self.dentistas.clicked.connect(self.show_dentists)

    def show_users(self):
        self.crud_users_window = CrudWindow()
        self.crud_users_window.show()

    def show_dentists(self):
        self.crud_dentists_window = CrudWindowDentists()
        self.crud_dentists_window.show()


class CrudWindow(QMainWindow):
    def __init__(self):
        super(CrudWindow, self).__init__()
        loadUi("CrudWindow.ui", self)

        # Configuración inicial de la tabla
        self.tableWidget.setColumnCount(6)
        self.tableWidget.setHorizontalHeaderLabels(
            ["ID", "Nombre", "Apellido", "Edad", "Dirección", "Email"]
        )

        self.load_data()

        # Conectar botones a las funciones CRUD
        self.btn_add.clicked.connect(self.add_user)
        self.btn_update.clicked.connect(self.update_user)
        self.btn_delete.clicked.connect(self.delete_user)
        self.btn_refresh.clicked.connect(self.load_data)

    def connect_db(self):
        return mysql.connector.connect(
            host="localhost", user="root", password="", database="Clinica"
        )

    def load_data(self):
        # Cargar datos en la tabla
        try:
            conn = self.connect_db()
            query = "SELECT id, nombre, apellido, edad, direccion, email FROM usuarios"
            cursor = conn.cursor()
            cursor.execute(query)
            rows = cursor.fetchall()
            conn.close()

            self.tableWidget.setRowCount(0)
            for row_number, row_data in enumerate(rows):
                self.tableWidget.insertRow(row_number)
                for column_number, data in enumerate(row_data):
                    self.tableWidget.setItem(row_number, column_number, QTableWidgetItem(str(data)))
        except Exception as e:
            QMessageBox.critical(self, "Error", f"No se pudo cargar la tabla.\n{e}")

    def add_user(self):
        """Agrega un nuevo usuario a la base de datos."""
        nombre = self.lineEdit_nombre.text()
        apellido = self.lineEdit_apellido.text()
        edad = self.spinBox_edad.value()
        direccion = self.lineEdit_direccion.text()
        email = self.lineEdit_email.text()
        contrasenia=self.lineEdit_contra.text()

        if not nombre or not apellido or not email:
            QMessageBox.warning(self, "Advertencia", "Los campos 'Nombre', 'Apellido' y 'Email' son obligatorios.")
            return

        try:
            conn = self.connect_db()
            query = """
                INSERT INTO usuarios (nombre, apellido, edad, direccion, email,contrasenia)
                VALUES (%s, %s, %s, %s, %s,%s)
            """
            data = (nombre, apellido, edad, direccion, email,contrasenia)
            cursor = conn.cursor()
            cursor.execute(query, data)
            conn.commit()
            conn.close()

            QMessageBox.information(self, "Éxito", "Usuario agregado correctamente.")
            self.load_data()  # Actualiza la tabla
        except Exception as e:
            QMessageBox.critical(self, "Error", f"No se pudo agregar el usuario.\n{e}")

    def update_user(self):
        """Actualiza los datos de un usuario seleccionado."""
        current_row = self.tableWidget.currentRow()
        if current_row == -1:
            QMessageBox.warning(self, "Advertencia", "Selecciona un usuario para actualizar.")
            return

        # Obtener el ID del usuario seleccionado
        user_id = self.tableWidget.item(current_row, 0).text()
        nombre = self.lineEdit_nombre.text()
        apellido = self.lineEdit_apellido.text()
        edad = self.spinBox_edad.value()
        direccion = self.lineEdit_direccion.text()
        email = self.lineEdit_email.text()

        if not nombre or not apellido or not email:
            QMessageBox.warning(self, "Advertencia", "Los campos 'Nombre', 'Apellido' y 'Email' son obligatorios.")
            return

        try:
            conn = self.connect_db()
            query = """
                UPDATE usuarios
                SET nombre=%s, apellido=%s, edad=%s, direccion=%s, email=%s
                WHERE id=%s
            """
            data = (nombre, apellido, edad, direccion, email, user_id)
            cursor = conn.cursor()
            cursor.execute(query, data)
            conn.commit()
            conn.close()

            QMessageBox.information(self, "Éxito", "Usuario actualizado correctamente.")
            self.load_data() 
        except Exception as e:
            QMessageBox.critical(self, "Error", f"No se pudo actualizar el usuario.\n{e}")

    def delete_user(self):
        """Elimina un usuario seleccionado."""
        current_row = self.tableWidget.currentRow()
        if current_row == -1:
            QMessageBox.warning(self, "Advertencia", "Selecciona un usuario para eliminar.")
            return

        # Obtener el ID del usuario seleccionado
        user_id = self.tableWidget.item(current_row, 0).text()

        # Confirmar eliminación
        confirm = QMessageBox.question(
            self, "Confirmación", "¿Estás seguro de que deseas eliminar este usuario?",
            QMessageBox.Yes | QMessageBox.No
        )

        if confirm == QMessageBox.No:
            return

        try:
            conn = self.connect_db()
            query = "DELETE FROM usuarios WHERE id=%s"
            cursor = conn.cursor()
            cursor.execute(query, (user_id,))
            conn.commit()
            conn.close()

            QMessageBox.information(self, "Éxito", "Usuario eliminado correctamente.")
            self.load_data()  # Actualiza la tabla
        except Exception as e:
            QMessageBox.critical(self, "Error", f"No se pudo eliminar el usuario.\n{e}")

class CrudWindowDentists(QMainWindow):
    def __init__(self):
        super(CrudWindowDentists, self).__init__()
        loadUi("CrudDentista.ui", self)

        self.tableWidget.setColumnCount(7)
        self.tableWidget.setHorizontalHeaderLabels(
            ["ID", "Nombre", "Apellido", "Edad", "Dirección", "Email", "Licencia"]
        )

        self.load_data()

        # Conectar botones a las funciones CRUD
        self.btn_add.clicked.connect(self.add_dentist)
        self.btn_update.clicked.connect(self.update_dentist)
        self.btn_delete.clicked.connect(self.delete_dentist)
        self.btn_refresh.clicked.connect(self.load_data)

    def connect_db(self):
        return mysql.connector.connect(
            host="localhost", user="root", password="", database="Clinica"
        )

    def load_data(self):
        # Cargar datos en la tabla
        try:
            conn = self.connect_db()
            query = "SELECT id, nombre, apellido, edad, direccion, email, licencia FROM dentistas"
            cursor = conn.cursor()
            cursor.execute(query)
            rows = cursor.fetchall()
            conn.close()

            self.tableWidget.setRowCount(0)
            for row_number, row_data in enumerate(rows):
                self.tableWidget.insertRow(row_number)
                for column_number, data in enumerate(row_data):
                    self.tableWidget.setItem(row_number, column_number, QTableWidgetItem(str(data)))
        except Exception as e:
            QMessageBox.critical(self, "Error", f"No se pudo cargar la tabla.\n{e}")

    def connect_db(self):
        return mysql.connector.connect(
            host="localhost", user="root", password="", database="Clinica"
        )

    def load_data(self):
        """Carga los datos de la base de datos en la tabla."""
        try:
            conn = self.connect_db()
            query = "SELECT id, nombre, apellido, edad, direccion, email, licencia FROM dentistas"
            cursor = conn.cursor()
            cursor.execute(query)
            rows = cursor.fetchall()
            conn.close()

            self.tableWidget.setRowCount(0)
            for row_number, row_data in enumerate(rows):
                self.tableWidget.insertRow(row_number)
                for column_number, data in enumerate(row_data):
                    self.tableWidget.setItem(row_number, column_number, QTableWidgetItem(str(data)))
        except Exception as e:
            QMessageBox.critical(self, "Error", f"No se pudo cargar la tabla.\n{e}")

    def add_dentist(self):
        """Agrega un nuevo dentista a la base de datos."""
        nombre = self.lineEdit_nombre.text()
        apellido = self.lineEdit_apellido.text()
        edad = self.spinBox_edad.value()
        direccion = self.lineEdit_direccion.text()
        email = self.lineEdit_email.text()
        licencia = self.lineEdit_licencia.text()

        if not nombre or not apellido or not email or not licencia:
            QMessageBox.warning(self, "Advertencia", "Los campos 'Nombre', 'Apellido', 'Email' y 'Licencia' son obligatorios.")
            return

        try:
            conn = self.connect_db()
            query = """
                INSERT INTO dentistas (nombre, apellido, edad, direccion, email, licencia)
                VALUES (%s, %s, %s, %s, %s, %s)
            """
            data = (nombre, apellido, edad, direccion, email, licencia)
            cursor = conn.cursor()
            cursor.execute(query, data)
            conn.commit()
            conn.close()

            QMessageBox.information(self, "Éxito", "Dentista agregado correctamente.")
            self.load_data()
        except Exception as e:
            QMessageBox.critical(self, "Error", f"No se pudo agregar el dentista.\n{e}")

    def update_dentist(self):
        """Actualiza los datos de un dentista seleccionado."""
        current_row = self.tableWidget.currentRow()
        if current_row == -1:
            QMessageBox.warning(self, "Advertencia", "Selecciona un dentista para actualizar.")
            return

        dentist_id = self.tableWidget.item(current_row, 0).text()
        nombre = self.lineEdit_nombre.text()
        apellido = self.lineEdit_apellido.text()
        edad = self.spinBox_edad.value()
        direccion = self.lineEdit_direccion.text()
        email = self.lineEdit_email.text()
        licencia = self.lineEdit_licencia.text()

        if not nombre or not apellido or not email or not licencia:
            QMessageBox.warning(self, "Advertencia", "Los campos 'Nombre', 'Apellido', 'Email' y 'Licencia' son obligatorios.")
            return

        try:
            conn = self.connect_db()
            query = """
                UPDATE dentistas
                SET nombre=%s, apellido=%s, edad=%s, direccion=%s, email=%s, licencia=%s
                WHERE id=%s
            """
            data = (nombre, apellido, edad, direccion, email, licencia, dentist_id)
            cursor = conn.cursor()
            cursor.execute(query, data)
            conn.commit()
            conn.close()

            QMessageBox.information(self, "Éxito", "Dentista actualizado correctamente.")
            self.load_data() 
        except Exception as e:
            QMessageBox.critical(self, "Error", f"No se pudo actualizar el dentista.\n{e}")

    def delete_dentist(self):
        """Elimina un dentista seleccionado."""
        current_row = self.tableWidget.currentRow()
        if current_row == -1:
            QMessageBox.warning(self, "Advertencia", "Selecciona un dentista para eliminar.")
            return

        dentist_id = self.tableWidget.item(current_row, 0).text()

        confirm = QMessageBox.question(
            self, "Confirmación", "¿Estás seguro de que deseas eliminar este dentista?",
            QMessageBox.Yes | QMessageBox.No
        )

        if confirm == QMessageBox.No:
            return

        try:
            conn = self.connect_db()
            query = "DELETE FROM dentistas WHERE id=%s"
            cursor = conn.cursor()
            cursor.execute(query, (dentist_id,))
            conn.commit()
            conn.close()

            QMessageBox.information(self, "Éxito", "Dentista eliminado correctamente.")
            self.load_data()
        except Exception as e:
            QMessageBox.critical(self, "Error", f"No se pudo eliminar el dentista.\n{e}")


def main():
    app = QApplication(sys.argv)
    window = MainApp()
    window.show()
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()

