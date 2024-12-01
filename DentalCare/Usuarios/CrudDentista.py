import sys
import mysql.connector
from PyQt5.QtWidgets import QApplication, QMainWindow, QMessageBox, QTableWidgetItem
from PyQt5.uic import loadUi
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

class CrudWindowDentists(QMainWindow):
    def __init__(self):
        super(CrudWindowDentists, self).__init__()
        # Obtener la ruta absoluta de Login.ui
        ui_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "CrudDentista.ui")
        
        # Cargar la interfaz
        loadUi(ui_path, self)

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
def showCrudDentista():
    app = QApplication(sys.argv)
    window = CrudWindowDentists()
    window.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    showCrudDentista()
