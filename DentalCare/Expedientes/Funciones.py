import os
import mysql.connector
from PyQt5 import QtWidgets
from PyQt5.uic import loadUi
from PyQt5.QtWidgets import QMessageBox
from PyQt5.QtCore import QDate

class MainWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        ruta_ui = os.path.join(os.path.dirname(__file__), "Interfaz.ui")
        loadUi(ruta_ui, self)

        # Conectar elementos de la interfaz
        self.patientComboBox = self.findChild(QtWidgets.QComboBox, "patientComboBox")
        self.treatmentComboBox = self.findChild(QtWidgets.QComboBox, "treatmentComboBox")
        self.treatmentNameLineEdit = self.findChild(QtWidgets.QLineEdit, "treatmentNameLineEdit")
        self.treatmentDetailsTextEdit = self.findChild(QtWidgets.QTextEdit, "treatmentDetails")
        self.nameLineEdit = self.findChild(QtWidgets.QLineEdit, "nameLineEdit")
        self.lastNameLineEdit = self.findChild(QtWidgets.QLineEdit, "lastNameLineEdit")
        self.dobDateEdit = self.findChild(QtWidgets.QDateEdit, "dobDateEdit")
        self.phoneLineEdit = self.findChild(QtWidgets.QLineEdit, "phoneLineEdit")
        self.emailLineEdit = self.findChild(QtWidgets.QLineEdit, "emailLineEdit")
        self.addressLineEdit = self.findChild(QtWidgets.QLineEdit, "addressLineEdit")
        self.addPatientButton = self.findChild(QtWidgets.QPushButton, "addPatientButton")
        self.saveButton = self.findChild(QtWidgets.QPushButton, "saveButton")
        self.deletePatientButton = self.findChild(QtWidgets.QPushButton, "deletePatientButton")
        self.cancelButton = self.findChild(QtWidgets.QPushButton, "cancelButton")

        self.addPatientButton.clicked.connect(self.add_new_patient)

        # Conectar señales
        self.patientComboBox.currentIndexChanged.connect(self.load_patient_data)
        self.treatmentComboBox.currentIndexChanged.connect(self.load_treatment_data)
        self.saveButton.clicked.connect(self.save_changes)
        self.deletePatientButton.clicked.connect(self.delete_treatment)
        self.cancelButton.clicked.connect(self.cancel)

        # Inicializar valores
        self.load_patients()

    def add_new_patient(self):
        """Añade un nuevo paciente si se cumplen las validaciones."""
        name = self.nameLineEdit.text().strip()
        last_name = self.lastNameLineEdit.text().strip()
        dob = self.dobDateEdit.date().toPyDate()
        phone = self.phoneLineEdit.text().strip()
        email = self.emailLineEdit.text().strip()
        address = self.addressLineEdit.text().strip()

        # Validaciones
        current_year = QDate.currentDate().year()
        if dob.year > current_year:
            QMessageBox.warning(self, "Error", "El año de nacimiento no puede ser mayor al año actual.")
            return

        if len(phone) < 10 or not phone.isdigit():
            QMessageBox.warning(self, "Error", "El teléfono debe tener al menos 10 dígitos y solo contener números.")
            return

        if "@" not in email or email.strip() == "":
            QMessageBox.warning(self, "Error", "Debe ingresar un correo electrónico válido.")
            return

        if not name or not last_name or not address:
            QMessageBox.warning(self, "Error", "Todos los campos son obligatorios.")
            return

        # Insertar el nuevo paciente en la base de datos
        connection = self.connect_to_db()
        cursor = connection.cursor()

        try:
            cursor.execute(
                """
                INSERT INTO Pacientes (nombre, apellido, fecha_nacimiento, telefono, correo, direccion)
                VALUES (%s, %s, %s, %s, %s, %s)
                """,
                (name, last_name, dob, phone, email, address)
            )
            connection.commit()
            QMessageBox.information(self, "Éxito", "El nuevo paciente ha sido añadido correctamente.")

            # Recargar la lista de pacientes
            self.load_patients()
            self.clear_fields()

        except mysql.connector.Error as err:
            QMessageBox.critical(self, "Error de Base de Datos", f"Ocurrió un error: {err}")
            connection.rollback()

        finally:
            connection.close()


    def connect_to_db(self):
        """Establece conexión a la base de datos MySQL."""
        return mysql.connector.connect(
            host="localhost",
            user="root",
            password="",
            database="clinica"
        )

    def load_patients(self):
        """Carga los pacientes en el ComboBox."""
        self.patientComboBox.clear()
        self.patientComboBox.addItem("Nuevo Paciente")

        connection = self.connect_to_db()
        cursor = connection.cursor()

        cursor.execute("SELECT id, CONCAT(nombre, ' ', apellido) AS nombre_completo FROM Pacientes")
        patients = cursor.fetchall()

        for patient_id, patient_name in patients:
            self.patientComboBox.addItem(patient_name, patient_id)

        connection.close()

    def load_treatments(self, patient_id):
        """Carga los tratamientos en el ComboBox."""
        self.treatmentComboBox.clear()
        self.treatmentComboBox.addItem("Nuevo Tratamiento")

        if not patient_id:
            return

        connection = self.connect_to_db()
        cursor = connection.cursor()

        cursor.execute("SELECT id, descripcion FROM Tratamientos WHERE id_paciente = %s", (patient_id,))
        treatments = cursor.fetchall()

        for treatment_id, treatment_description in treatments:
            self.treatmentComboBox.addItem(treatment_description, treatment_id)

        connection.close()

    def load_patient_data(self):
        """Carga los datos del paciente seleccionado y sus tratamientos."""
        if self.patientComboBox.currentText() == "Nuevo Paciente":
            self.clear_fields()
            self.set_fields_editable(True)
            self.addPatientButton.setVisible(True)
            self.load_treatments(None)
            return

        patient_id = self.patientComboBox.currentData()

        connection = self.connect_to_db()
        cursor = connection.cursor()

        cursor.execute("""
            SELECT nombre, apellido, fecha_nacimiento, telefono, correo, direccion
            FROM Pacientes
            WHERE id = %s
        """, (patient_id,))
        patient = cursor.fetchone()

        if patient:
            self.nameLineEdit.setText(patient[0])
            self.lastNameLineEdit.setText(patient[1])
            dob_str = patient[2].strftime("%Y-%m-%d") if patient[2] else None
            if dob_str:
                self.dobDateEdit.setDate(QDate.fromString(dob_str, "yyyy-MM-dd"))
            self.phoneLineEdit.setText(patient[3])
            self.emailLineEdit.setText(patient[4])
            self.addressLineEdit.setText(patient[5])
            self.set_fields_editable(False)
            self.addPatientButton.setVisible(False)
            self.load_treatments(patient_id)
        else:
            QMessageBox.warning(self, "Error", "No se encontraron datos para el paciente seleccionado.")

        connection.close()

    def load_treatment_data(self):
        """Carga los datos del tratamiento seleccionado."""
        if self.treatmentComboBox.currentText() == "Nuevo Tratamiento":
            self.treatmentNameLineEdit.setReadOnly(False)
            self.treatmentNameLineEdit.clear()
            self.treatmentDetailsTextEdit.clear()
        else:
            treatment_id = self.treatmentComboBox.currentData()
            if not treatment_id:
                return

            connection = self.connect_to_db()
            cursor = connection.cursor()

            try:
                # Obtener la descripción del progreso más reciente del tratamiento
                cursor.execute("""
                    SELECT descripcion 
                    FROM ProgresoTratamiento 
                    WHERE id_tratamiento = %s
                    ORDER BY fecha DESC
                    LIMIT 1
                """, (treatment_id,))
                progress_description = cursor.fetchone()

                # Mostrar el nombre del tratamiento y su progreso
                self.treatmentNameLineEdit.setText(self.treatmentComboBox.currentText())
                self.treatmentNameLineEdit.setReadOnly(True)

                if progress_description and progress_description[0]:
                    self.treatmentDetailsTextEdit.setText(progress_description[0])
                else:
                    self.treatmentDetailsTextEdit.clear()
                    QMessageBox.information(self, "Información", "El tratamiento no tiene progreso asociado.")

            except mysql.connector.Error as err:
                QMessageBox.critical(self, "Error", f"Error al cargar el tratamiento: {err}")
            finally:
                connection.close()

    def clear_fields(self):
        """Limpia los campos para un nuevo paciente."""
        self.nameLineEdit.clear()
        self.lastNameLineEdit.clear()
        self.dobDateEdit.setDate(QDate.currentDate())
        self.phoneLineEdit.clear()
        self.emailLineEdit.clear()
        self.addressLineEdit.clear()
        self.treatmentNameLineEdit.clear()
        self.treatmentDetailsTextEdit.clear()

    def set_fields_editable(self, editable):
        """Habilita o deshabilita la edición de los campos."""
        self.nameLineEdit.setReadOnly(not editable)
        self.lastNameLineEdit.setReadOnly(not editable)
        self.dobDateEdit.setReadOnly(not editable)
        self.phoneLineEdit.setReadOnly(not editable)
        self.emailLineEdit.setReadOnly(not editable)
        self.addressLineEdit.setReadOnly(not editable)

    def save_changes(self):
        """Guarda los cambios en la base de datos."""
        connection = self.connect_to_db()
        cursor = connection.cursor()

        try:
            # Obtener el ID del paciente seleccionado
            patient_id = self.patientComboBox.currentData()
            if not patient_id:
                QMessageBox.warning(self, "Error", "Debe seleccionar un paciente válido.")
                return

            # Validar el tratamiento
            if self.treatmentComboBox.currentText() == "Nuevo Tratamiento":
                new_treatment_name = self.treatmentNameLineEdit.text().strip()
                if not new_treatment_name:
                    QMessageBox.warning(self, "Error", "Debe ingresar un nombre para el nuevo tratamiento.")
                    return

                # Insertar el nuevo tratamiento
                cursor.execute(
                    "INSERT INTO Tratamientos (id_paciente, descripcion) VALUES (%s, %s)",
                    (patient_id, new_treatment_name)
                )
                treatment_id = cursor.lastrowid
            else:
                treatment_id = self.treatmentComboBox.currentData()

            # Guardar el progreso del tratamiento
            treatment_progress_description = self.treatmentDetailsTextEdit.toPlainText().strip()
            if treatment_progress_description:
                cursor.execute(
                    "INSERT INTO ProgresoTratamiento (id_tratamiento, descripcion) VALUES (%s, %s)",
                    (treatment_id, treatment_progress_description)
                )

            # Confirmar cambios
            connection.commit()
            QMessageBox.information(self, "Éxito", "Los cambios se han guardado correctamente.")

            # Recargar los tratamientos para el paciente seleccionado
            self.load_treatments(patient_id)

            # Restablecer el ComboBox a "Nuevo Tratamiento"
            self.treatmentComboBox.setCurrentIndex(0)
            self.treatmentNameLineEdit.clear()
            self.treatmentDetailsTextEdit.clear()

        except mysql.connector.Error as err:
            QMessageBox.critical(self, "Error de Base de Datos", f"Ocurrió un error: {err}")
            connection.rollback()

        finally:
            connection.close()

    def delete_treatment(self):
        """Elimina el tratamiento seleccionado de la base de datos."""
        connection = self.connect_to_db()
        cursor = connection.cursor()

        try:
            # Obtener el ID del tratamiento seleccionado
            treatment_id = self.treatmentComboBox.currentData()  # O el método adecuado para obtener el ID del tratamiento.
            if not treatment_id:
                QMessageBox.warning(self, "Error", "Debe seleccionar un tratamiento válido.")
                return

            # Confirmar eliminación con el usuario
            reply = QMessageBox.question(self, "Confirmar Eliminación", 
                                        "¿Está seguro de que desea eliminar este tratamiento?", 
                                        QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
            if reply == QMessageBox.No:
                return

            # Eliminar el tratamiento de la base de datos
            cursor.execute("DELETE FROM ProgresoTratamiento WHERE id_tratamiento = %s", (treatment_id,))
            cursor.execute("DELETE FROM Tratamientos WHERE id = %s", (treatment_id,))

            # Confirmar cambios
            connection.commit()
            QMessageBox.information(self, "Éxito", "El tratamiento ha sido eliminado correctamente.")

            # Recargar los tratamientos para el paciente seleccionado
            patient_id = self.patientComboBox.currentData()
            self.load_treatments(patient_id)

            # Restablecer el ComboBox a "Nuevo Tratamiento"
            self.treatmentComboBox.setCurrentIndex(0)
            self.treatmentNameLineEdit.clear()
            self.treatmentDetailsTextEdit.clear()

        except mysql.connector.Error as err:
            QMessageBox.critical(self, "Error de Base de Datos", f"Ocurrió un error: {err}")
            connection.rollback()

        finally:
            connection.close()

    def cancel(self):
        reply = QMessageBox.question(
            self,
            "Confirmar salida",
            "¿Estás seguro de que deseas salir de los tratamientos?",
            QMessageBox.Yes | QMessageBox.No,
            QMessageBox.No
        )
        if reply == QMessageBox.Yes:
            self.close()
        
if __name__ == "__main__":
    import sys

    app = QtWidgets.QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())

