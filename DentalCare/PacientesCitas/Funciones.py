import os
import mysql.connector
from PyQt5.uic import loadUi
from PyQt5.QtWidgets import QApplication, QMainWindow, QTableWidgetItem
from PyQt5.QtGui import QColor, QBrush
from PyQt5.QtCore import Qt
from datetime import datetime, timedelta, date, time

class SemanaApp(QMainWindow):
    def __init__(self):
        super().__init__()
        ruta_ui = os.path.join(os.path.dirname(__file__), "Opcion4.ui")
        loadUi(ruta_ui, self)

        self.inicio_semana = (datetime.now() - timedelta(days=datetime.now().weekday())).date()

        self.btnSiguiente.clicked.connect(self.mostrarSiguienteSemana)
        self.btnAnterior.clicked.connect(self.mostrarSemanaAnterior)
        self.tableWidgetSemana.cellClicked.connect(self.mostrarDetallesCita)  # Conectar el evento

        self.actualizarFechas()

    def conectar_db(self):
        return mysql.connector.connect(
            host="localhost",
            user="root",
            password="",
            database="clinica"
        )

    def actualizarFechas(self):
        for i in range(7):  # 7 días de la semana
            fecha = self.inicio_semana + timedelta(days=i)
            self.tableWidgetSemana.setHorizontalHeaderItem(i, QTableWidgetItem(fecha.strftime("%d - %A")))

        self.tableWidgetSemana.clearContents()
        self.desactivarCeldasPasadas()
        self.cargarCitas()
        self.mostrarHorasDisponibles()

    def desactivarCeldasPasadas(self):
        hora_actual = datetime.now().time()
        fecha_actual = datetime.now().date()

        for dia in range(7):  # 7 días de la semana
            fecha_celda = self.inicio_semana + timedelta(days=dia)
            for hora_index, hora in enumerate([
                "07:00:00", "08:00:00", "09:00:00", "10:00:00", "11:00:00",
                "12:00:00", "13:00:00", "14:00:00", "15:00:00", "16:00:00",
                "17:00:00", "18:00:00", "19:00:00"
            ]):
                hora_celda = datetime.strptime(hora, "%H:%M:%S").time()

                if fecha_celda < fecha_actual or (fecha_celda == fecha_actual and hora_celda <= hora_actual):
                    item = QTableWidgetItem("")
                    item.setFlags(Qt.ItemIsSelectable | Qt.ItemIsEnabled)
                    item.setBackground(QBrush(QColor(200, 200, 200)))
                    self.tableWidgetSemana.setItem(hora_index, dia, item)

    def cargarCitas(self):
        try:
            conn = self.conectar_db()
            cursor = conn.cursor()

            fecha_inicio = self.inicio_semana.strftime("%Y-%m-%d")
            fecha_fin = (self.inicio_semana + timedelta(days=6)).strftime("%Y-%m-%d")
            query = """
                SELECT CitasMedicas.fecha, CitasMedicas.hora, Pacientes.nombre, 
                    CitasMedicas.motivo, CitasMedicas.estado, dentistas.nombre
                FROM CitasMedicas
                JOIN Pacientes ON CitasMedicas.id_paciente = Pacientes.id
                JOIN dentistas ON CitasMedicas.id_dentista = dentistas.id
                WHERE CitasMedicas.fecha BETWEEN %s AND %s
            """
            cursor.execute(query, (fecha_inicio, fecha_fin))
            self.citas = cursor.fetchall()

            for cita in self.citas:
                fecha, hora, nombre_paciente, motivo, estado, dentista = cita
            
                # Ignorar citas con estado "Cancelada"
                if estado.lower() == "cancelada":
                    continue

                fecha_date = fecha if isinstance(fecha, date) else fecha.date()
                dia_semana = (fecha_date - self.inicio_semana).days

                hora_str = (datetime.min + hora).strftime("%H:%M:%S")
                hora_index = self.hora_a_indice(hora_str)

                if 0 <= dia_semana < 7 and 0 <= hora_index < 13:
                    # Crear el QTableWidgetItem con el nombre del paciente
                    item = QTableWidgetItem(nombre_paciente)

                    # Asignar color de fondo según el estado
                    if estado.lower() == "pendiente":
                        item.setBackground(QBrush(QColor(255, 165, 0)))  # Naranja
                    elif estado.lower() == "confirmada":
                        item.setBackground(QBrush(QColor(0, 102, 204)))  # Azul oscuro

                    # Establecer el texto en blanco y centrarlo
                    item.setForeground(QBrush(QColor(255, 255, 255)))  # Texto blanco
                    item.setTextAlignment(Qt.AlignCenter)
                    self.tableWidgetSemana.setItem(hora_index, dia_semana, item)

            conn.close()
        except Exception as e:
            print(f"Error al cargar las citas: {e}")


    def mostrarDetallesCita(self, fila, columna):
        fecha_celda = self.inicio_semana + timedelta(days=columna)
        hora_celda = [
            "07:00:00", "08:00:00", "09:00:00", "10:00:00", "11:00:00",
            "12:00:00", "13:00:00", "14:00:00", "15:00:00", "16:00:00",
            "17:00:00", "18:00:00", "19:00:00"
        ][fila]

        # Buscar si hay una cita en la celda seleccionada
        cita_encontrada = False
        for cita in self.citas:
            fecha, hora, nombre_paciente, motivo, estado, dentista = cita
            hora_str = (datetime.min + hora).strftime("%H:%M:%S")

            if fecha == fecha_celda and hora_str == hora_celda:
                # Cita encontrada, actualizar el panel con los datos de la cita
                self.lineEditPaciente.setText(nombre_paciente)
                self.lineEditMotivo.setText(motivo)
                self.dateEditFecha.setDate(fecha)
                self.timeEditHora.setTime(datetime.strptime(hora_str, "%H:%M:%S").time())
                self.comboBoxEstado.setCurrentText(estado.capitalize())

                # Actualizar el comboBoxDentista
                if dentista not in [self.comboBoxDentista.itemText(i) for i in range(self.comboBoxDentista.count())]:
                    self.comboBoxDentista.addItem(dentista)

                self.comboBoxDentista.setCurrentText(dentista)
                cita_encontrada = True
                break

        if not cita_encontrada:
            # Si no hay cita, actualizar el panel con la fecha y hora seleccionadas
            self.lineEditPaciente.clear()
            self.lineEditMotivo.clear()
            self.dateEditFecha.setDate(fecha_celda)
            self.timeEditHora.setTime(datetime.strptime(hora_celda, "%H:%M:%S").time())
            self.comboBoxEstado.setCurrentIndex(-1)  # Desseleccionar el estado
            self.comboBoxDentista.setCurrentIndex(-1)  # Desseleccionar el dentista

    def mostrarHorasDisponibles(self):
        horas_disponibles = 0
        hora_actual = datetime.now().time()
        fecha_actual = datetime.now().date()

        for dia in range(7):  # 7 días de la semana
            fecha_celda = self.inicio_semana + timedelta(days=dia)
            for hora_index, hora in enumerate([
                "07:00:00", "08:00:00", "09:00:00", "10:00:00", "11:00:00",
                "12:00:00", "13:00:00", "14:00:00", "15:00:00", "16:00:00",
                "17:00:00", "18:00:00", "19:00:00"
            ]):
                hora_celda = datetime.strptime(hora, "%H:%M:%S").time()
                item = self.tableWidgetSemana.item(hora_index, dia)
                if fecha_celda >= fecha_actual and (fecha_celda > fecha_actual or hora_celda > hora_actual):
                    if item is None or not item.text():
                        horas_disponibles += 1

        self.labelHorasDisponibles.setText(f"Horas disponibles en la semana: {horas_disponibles}")

    def hora_a_indice(self, hora):
        horas = [
            "07:00:00", "08:00:00", "09:00:00", "10:00:00", "11:00:00",
            "12:00:00", "13:00:00", "14:00:00", "15:00:00", "16:00:00",
            "17:00:00", "18:00:00", "19:00:00"
        ]
        try:
            return horas.index(hora)
        except ValueError:
            return -1

    def mostrarSiguienteSemana(self):
        self.inicio_semana += timedelta(weeks=1)
        self.actualizarFechas()

    def mostrarSemanaAnterior(self):
        self.inicio_semana -= timedelta(weeks=1)
        self.actualizarFechas()

if __name__ == "__main__":
    app = QApplication([])
    window = SemanaApp()
    window.show()
    app.exec_()
