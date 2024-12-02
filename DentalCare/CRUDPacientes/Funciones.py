import os
import sys
from PyQt5.QtWidgets import QMainWindow, QApplication, QMessageBox, QTableWidgetItem
from PyQt5.uic import loadUi
import mysql.connector
from datetime import datetime


class PacientesCRUD(QMainWindow):
    def __init__(self):
        super().__init__()
        ruta_ui = os.path.join(os.path.dirname(__file__), "Interfaz.ui")
        loadUi(ruta_ui, self)

        # Conectar botones a funciones
        self.btn_add.clicked.connect(self.agregar_paciente)
        self.btn_guardar.clicked.connect(self.guardar_cambios)
        self.btn_eliminar.clicked.connect(self.eliminar_paciente)

        # Inicialmente ocultar botones Guardar y Eliminar
        self.btn_guardar.setVisible(False)
        self.btn_eliminar.setVisible(False)
        self.btn_add.setText("Agregar")  # Inicia como "Agregar"

        # Conectar selección de la tabla
        self.tableWidget.cellClicked.connect(self.cargar_detalles_paciente)

        # Cargar datos iniciales
        self.cargar_pacientes()

    def conectar_db(self):
        """Establece conexión con la base de datos."""
        return mysql.connector.connect(
            host="localhost",
            user="root",
            password="",
            database="clinica"
        )

    def cargar_pacientes(self):
        """Carga los pacientes desde la base de datos en la tabla."""
        try:
            conn = self.conectar_db()
            cursor = conn.cursor()
            query = """
                SELECT id, nombre, apellido, direccion, correo, telefono, 
                       TIMESTAMPDIFF(YEAR, fecha_nacimiento, CURDATE()) AS edad 
                FROM Pacientes
            """
            cursor.execute(query)
            pacientes = cursor.fetchall()
            conn.close()

            self.tableWidget.setRowCount(0)  # Limpiar la tabla
            for row_number, paciente in enumerate(pacientes):
                self.tableWidget.insertRow(row_number)
                for col_number, data in enumerate(paciente):
                    self.tableWidget.setItem(row_number, col_number, QTableWidgetItem(str(data)))

        except Exception as e:
            QMessageBox.critical(self, "Error", f"Error al cargar pacientes: {e}")

    def validar_datos(self, nombre, apellidos, telefono, correo, fecha_nacimiento):
        """Valida los datos ingresados por el usuario."""
        if not nombre or not apellidos or not telefono or not correo:
            QMessageBox.warning(self, "Campos Vacíos", "Todos los campos deben estar llenos.")
            return False

        if "@" not in correo:
            QMessageBox.warning(self, "Correo Inválido", "El correo debe contener '@'.")
            return False

        if len(telefono) < 10 or not telefono.isdigit():
            QMessageBox.warning(self, "Teléfono Inválido", "El número de teléfono debe tener al menos 10 dígitos.")
            return False

        if fecha_nacimiento.year > datetime.now().year:
            QMessageBox.warning(self, "Fecha Inválida", "El año de nacimiento no puede ser mayor al año actual.")
            return False

        return True

    def agregar_paciente(self):
        """Agrega un nuevo paciente o limpia los campos si el botón dice 'Limpiar'."""
        if self.btn_add.text() == "Limpiar":
            self.limpiar_campos()
            return

        nombre = self.lineEdit_nombre.text().strip()
        apellidos = self.lineEdit_apellidos.text().strip()
        fecha_nacimiento = self.dateEdit_nacimiento.date().toPyDate()
        telefono = self.lineEdit_telefono.text().strip()
        correo = self.lineEdit_email.text().strip()
        direccion = self.lineEdit_direccion.text().strip()

        if not self.validar_datos(nombre, apellidos, telefono, correo, fecha_nacimiento):
            return

        try:
            conn = self.conectar_db()
            cursor = conn.cursor()
            query = """
                INSERT INTO Pacientes (nombre, apellido, fecha_nacimiento, telefono, correo, direccion)
                VALUES (%s, %s, %s, %s, %s, %s)
            """
            cursor.execute(query, (nombre, apellidos, fecha_nacimiento, telefono, correo, direccion))
            conn.commit()
            conn.close()

            QMessageBox.information(self, "Éxito", "Paciente agregado correctamente.")
            self.cargar_pacientes()
            self.limpiar_campos()

        except Exception as e:
            QMessageBox.critical(self, "Error", f"Error al agregar paciente: {e}")

    def cargar_detalles_paciente(self, row, column):
        """Carga los datos del paciente seleccionado en los campos de texto."""
        try:
            self.lineEdit_nombre.setText(self.tableWidget.item(row, 1).text())
            self.lineEdit_apellidos.setText(self.tableWidget.item(row, 2).text())
            self.lineEdit_direccion.setText(self.tableWidget.item(row, 3).text())
            self.lineEdit_email.setText(self.tableWidget.item(row, 4).text())
            self.lineEdit_telefono.setText(self.tableWidget.item(row, 5).text())

            # Recuperar el ID del paciente para futuras operaciones
            self.paciente_id = int(self.tableWidget.item(row, 0).text())

            # Mostrar botones Guardar y Eliminar, cambiar el de Agregar a "Limpiar"
            self.btn_guardar.setVisible(True)
            self.btn_eliminar.setVisible(True)
            self.btn_add.setText("Limpiar")

        except Exception as e:
            QMessageBox.critical(self, "Error", f"Error al cargar detalles del paciente: {e}")

    def guardar_cambios(self):
        """Guarda los cambios realizados en el paciente seleccionado."""
        if not hasattr(self, "paciente_id"):
            QMessageBox.warning(self, "Sin Selección", "Por favor, selecciona un paciente para editar.")
            return

        nombre = self.lineEdit_nombre.text().strip()
        apellidos = self.lineEdit_apellidos.text().strip()
        fecha_nacimiento = self.dateEdit_nacimiento.date().toPyDate()
        telefono = self.lineEdit_telefono.text().strip()
        correo = self.lineEdit_email.text().strip()
        direccion = self.lineEdit_direccion.text().strip()

        if not self.validar_datos(nombre, apellidos, telefono, correo, fecha_nacimiento):
            return

        try:
            conn = self.conectar_db()
            cursor = conn.cursor()
            query = """
                UPDATE Pacientes
                SET nombre = %s, apellido = %s, fecha_nacimiento = %s, telefono = %s, correo = %s, direccion = %s
                WHERE id = %s
            """
            cursor.execute(query, (nombre, apellidos, fecha_nacimiento, telefono, correo, direccion, self.paciente_id))
            conn.commit()
            conn.close()

            QMessageBox.information(self, "Éxito", "Paciente actualizado correctamente.")
            self.cargar_pacientes()
            self.limpiar_campos()

        except Exception as e:
            QMessageBox.critical(self, "Error", f"Error al guardar cambios: {e}")

    def eliminar_paciente(self):
        """Elimina el paciente seleccionado."""
        if not hasattr(self, "paciente_id"):
            QMessageBox.warning(self, "Sin Selección", "Por favor, selecciona un paciente para eliminar.")
            return

        respuesta = QMessageBox.question(
            self, "Confirmar Eliminación", "¿Estás seguro de que deseas eliminar este paciente?",
            QMessageBox.Yes | QMessageBox.No
        )

        if respuesta == QMessageBox.Yes:
            try:
                conn = self.conectar_db()
                cursor = conn.cursor()
                query = "DELETE FROM Pacientes WHERE id = %s"
                cursor.execute(query, (self.paciente_id,))
                conn.commit()
                conn.close()

                QMessageBox.information(self, "Éxito", "Paciente eliminado correctamente.")
                self.cargar_pacientes()
                self.limpiar_campos()

            except Exception as e:
                QMessageBox.critical(self, "Error", f"Error al eliminar paciente: {e}")

    def limpiar_campos(self):
        """Limpia todos los campos de entrada y restablece botones."""
        self.lineEdit_nombre.clear()
        self.lineEdit_apellidos.clear()
        self.lineEdit_telefono.clear()
        self.lineEdit_email.clear()
        self.lineEdit_direccion.clear()
        self.dateEdit_nacimiento.clear()

        self.paciente_id = None

        # Ocultar botones Guardar y Eliminar, mostrar Agregar
        self.btn_guardar.setVisible(False)
        self.btn_eliminar.setVisible(False)
        self.btn_add.setText("Agregar")


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = PacientesCRUD()
    window.show()
    sys.exit(app.exec_())
