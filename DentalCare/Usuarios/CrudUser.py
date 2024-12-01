import sys
import mysql.connector
from PyQt5.QtWidgets import QApplication, QMainWindow, QMessageBox, QTableWidgetItem
from PyQt5.uic import loadUi
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

class CrudWindowUser(QMainWindow):
    def __init__(self):
        super(CrudWindowUser, self).__init__()
        # Obtener la ruta absoluta de Login.ui
        ui_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "CrudWindow.ui")
        
        # Cargar la interfaz
        loadUi(ui_path, self)

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

def showCrudUser():
    app = QApplication(sys.argv)
    window = CrudWindowUser()
    window.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    showCrudUser()
