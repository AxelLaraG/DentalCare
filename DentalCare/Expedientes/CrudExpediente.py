import sys
import mysql.connector
from PyQt5 import QtWidgets, uic
from PyQt5.QtWidgets import QApplication, QMainWindow, QMessageBox, QTableWidgetItem
from PyQt5.QtCore import QDate

# Cargar la interfaz desde el archivo .ui
class Form(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()

        # Cargar la interfaz del archivo .ui
        uic.loadUi('CrudExpediente.ui', self)  # Asegúrate de que el archivo .ui esté en la misma carpeta

        # Conectar señales y slots
        self.btn_generar_tratamiento.clicked.connect(self.generar_tratamiento)
        self.btn_buscar_paciente.clicked.connect(self.buscar_paciente)
        self.btn_dar_seguimiento.clicked.connect(self.dar_seguimiento)

        # Llenar el comboBox_paciente con los pacientes desde la base de datos
        self.cargar_pacientes()
        
    def connect_db(self):
        return mysql.connector.connect(
            host="localhost", user="root", password="", database="clinica"
        )

    def cargar_pacientes(self):
        try:
            conn = self.connect_db()  # Conectar a la base de datos
            query = "SELECT id, nombre FROM usuarios"  # Cambiar según tu tabla de pacientes
            cursor = conn.cursor()
            cursor.execute(query)
            pacientes = cursor.fetchall()
            conn.close()

            # Limpiar los combobox antes de agregar los nuevos elementos
            self.comboBox_paciente.clear()
            self.comboBox_paciente_2.clear()

            # Llenar los combobox con los pacientes obtenidos
            for paciente in pacientes:
                self.comboBox_paciente.addItem(paciente[1])  # Agregar solo el nombre al comboBox_paciente
                self.comboBox_paciente_2.addItem(paciente[1])  # Agregar solo el nombre al comboBox_paciente_2
        except Exception as e:
            QMessageBox.critical(self, "Error", f"No se pudo cargar los pacientes.\n{e}")

    def generar_tratamiento(self):
        paciente = self.comboBox_paciente.currentText()
        tratamiento = self.lineEdit_tratamiento.text()

        try:
            # Obtener el id del usuario seleccionado
            paciente_id = self.get_usuario_id(paciente)
            
            # Obtener la fecha actual en formato YYYY-MM-DD
            fecha_actual = QDate.currentDate().toString("yyyy-MM-dd")

            # Insertar los datos en la tabla tratamientos
            conn = self.connect_db()  # Conectar a la base de datos
            query = """
            INSERT INTO tratamientos (id_usuario, nombre_tratamiento, fecha_inicio, ultima_actualizacion)
            VALUES (?, ?, ?, ?)
            """
            cursor = conn.cursor()
            cursor.execute(query, (paciente_id, tratamiento, fecha_actual, fecha_actual))
            conn.commit()  # Confirmar la transacción
            conn.close()  # Cerrar la conexión

            QtWidgets.QMessageBox.information(self, "Éxito", "Tratamiento generado correctamente.")
        except Exception as e:
            QMessageBox.critical(self, "Error", f"No se pudo generar el tratamiento.\n{e}")

    def get_usuario_id(self, nombre_paciente):
        # Método para obtener el ID del paciente a partir de su nombre
        try:
            conn = self.connect_db()
            query = """SELECT id FROM usuarios WHERE nombre = ?"""
            cursor = conn.cursor()
            cursor.execute(query, (nombre_paciente,))
            paciente_id = cursor.fetchone()
            conn.close()
            
            if paciente_id:
                return paciente_id[0]
            else:
                raise ValueError("Paciente no encontrado.")
        except Exception as e:
            raise ValueError(f"No se pudo obtener el ID del paciente.\n{e}")


    def buscar_paciente(self):
        paciente = self.comboBox_paciente_2.currentText()
        query = "SELECT tratamiento, fecha_inicio, ultima_modificacion FROM tratamientos WHERE paciente = ?"
        self.cursor.execute(query, (paciente,))
        tratamientos = self.cursor.fetchall()

        self.tableWidget_expediente.setRowCount(0)  # Limpiar la tabla
        for row_num, row_data in enumerate(tratamientos):
            self.tableWidget_expediente.insertRow(row_num)
            for col_num, data in enumerate(row_data):
                self.tableWidget_expediente.setItem(row_num, col_num, QTableWidgetItem(str(data)))


    def dar_seguimiento(self):
        pass

    def closeEvent(self, event):
        
        event.accept()

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    window = Form()
    window.show()
    sys.exit(app.exec_())
