import os
import mysql.connector
from PyQt5.uic import loadUi
from PyQt5.QtWidgets import QApplication, QMainWindow, QTableWidgetItem, QHeaderView
from PyQt5.QtGui import QColor, QBrush
from PyQt5.QtCore import Qt
from datetime import datetime, timedelta, date, time

class SemanaApp(QMainWindow):
    def __init__(self):
        super().__init__()
        ruta_ui = os.path.join(os.path.dirname(__file__), "Interfaz.ui")
        loadUi(ruta_ui, self)

        # Ajustar el tamaño de las celdas y encabezados
        self.tableWidgetSemana.horizontalHeader().setDefaultSectionSize(120)  # Ancho predeterminado
        self.tableWidgetSemana.verticalHeader().setDefaultSectionSize(30)    # Altura predeterminada
        self.tableWidgetSemana.horizontalHeader().setSectionResizeMode(QHeaderView.Fixed)
        self.tableWidgetSemana.verticalHeader().setSectionResizeMode(QHeaderView.Fixed)

        self.inicio_semana = (datetime.now() - timedelta(days=datetime.now().weekday())).date()
        self.citas_por_celda = {}  
        self.citas_actuales = []  
        self.indice_cita_actual = 0  

        self.btnSiguiente.clicked.connect(self.mostrarSiguienteSemana)
        self.btnAnterior.clicked.connect(self.mostrarSemanaAnterior)
        self.tableWidgetSemana.cellClicked.connect(self.mostrarDetallesCita)  # Conectar el evento
        self.btnAnteriorDetalles.clicked.connect(self.mostrarCitaAnterior)
        self.btnSiguienteDetalles.clicked.connect(self.mostrarCitaSiguiente)

        self.actualizarFechas()
        self.cargarPacientes() 
        
    def conectar_db(self):
        return mysql.connector.connect(
            host="localhost",
            user="root",
            password="",
            database="clinica"
        )
    
    def cargarPacientes(self):
        try:
            conn = self.conectar_db()
            cursor = conn.cursor()
            query = "SELECT nombre FROM Pacientes"  # Asume que la tabla de pacientes se llama 'Pacientes'
            cursor.execute(query)
            pacientes = cursor.fetchall()

            self.comboBoxPaciente.clear()  # Limpia el combo box antes de agregar nuevos elementos

            for paciente in pacientes:
                self.comboBoxPaciente.addItem(paciente[0])  # Agregar cada nombre al combo box

            conn.close()
        except Exception as e:
            print(f"Error al cargar los pacientes: {e}")

    def cargarDentistasDisponibles(self, fecha, hora):
        try:
            conn = self.conectar_db()
            cursor = conn.cursor()
            
            # Consulta para obtener los dentistas disponibles
            query = """
                SELECT d.nombre
                FROM dentistas d
                WHERE d.id NOT IN (
                    SELECT c.id_dentista
                    FROM CitasMedicas c
                    WHERE c.fecha = %s AND c.hora = %s AND c.estado != 'cancelada'
                )
            """
            cursor.execute(query, (fecha, hora))
            dentistas = cursor.fetchall()

            # Limpieza del combo box
            self.comboBoxDentista.clear()

            # Agregar dentistas disponibles al combo box
            for dentista in dentistas:
                self.comboBoxDentista.addItem(dentista[0])

            conn.close()
        except Exception as e:
            print(f"Error al cargar los dentistas disponibles: {e}")

    def actualizarFechas(self):
        for i in range(7):  # 7 días de la semana
            fecha = self.inicio_semana + timedelta(days=i)
            self.tableWidgetSemana.setHorizontalHeaderItem(i, QTableWidgetItem(fecha.strftime("%d - %A")))

        # Establecer las horas en el encabezado vertical
        horas = [
            "07:00 AM", "08:00 AM", "09:00 AM", "10:00 AM", "11:00 AM",
            "12:00 PM", "01:00 PM", "02:00 PM", "03:00 PM", "04:00 PM",
            "05:00 PM", "06:00 PM", "07:00 PM"
        ]
        for i, hora in enumerate(horas):
            self.tableWidgetSemana.setVerticalHeaderItem(i, QTableWidgetItem(hora))

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

            self.citas_por_celda = {}

            for cita in self.citas:
                fecha, hora, nombre_paciente, motivo, estado, dentista = cita

                if estado.lower() == "cancelada":
                    continue

                fecha_date = fecha if isinstance(fecha, date) else fecha.date()
                dia_semana = (fecha_date - self.inicio_semana).days

                hora_str = (datetime.min + hora).strftime("%H:%M:%S")
                hora_index = self.hora_a_indice(hora_str)

                if 0 <= dia_semana < 7 and 0 <= hora_index < 13:
                    clave_celda = (hora_index, dia_semana)
                    if clave_celda not in self.citas_por_celda:
                        self.citas_por_celda[clave_celda] = []
                    self.citas_por_celda[clave_celda].append(cita)

                    # Mostrar el nombre del primer paciente y "+N" si hay más citas
                    primer_paciente = self.citas_por_celda[clave_celda][0][2]
                    total_citas = len(self.citas_por_celda[clave_celda])
                    texto_celda = primer_paciente
                    if total_citas > 1:
                        texto_celda += f" +{total_citas - 1}"

                    item = QTableWidgetItem(texto_celda)

                    # Asignar color según el estado de la primera cita
                    primer_estado = self.citas_por_celda[clave_celda][0][4]
                    if primer_estado.lower() == "pendiente":
                        item.setBackground(QBrush(QColor(255, 140, 0)))  # Naranja oscuro
                    elif primer_estado.lower() == "confirmada":
                        item.setBackground(QBrush(QColor(0, 102, 204)))  # Azul oscuro

                    item.setForeground(QBrush(QColor(255, 255, 255)))  # Texto blanco
                    item.setTextAlignment(Qt.AlignCenter)
                    self.tableWidgetSemana.setItem(hora_index, dia_semana, item)

            conn.close()
        except Exception as e:
            print(f"Error al cargar las citas: {e}")

    def actualizarCeldaCita(self, fila, columna, cita):
        nombre_paciente, estado = cita[2], cita[4]
        texto_celda = nombre_paciente
        if len(self.citas_por_celda.get((fila, columna), [])) > 1:
            texto_celda += f" +{len(self.citas_por_celda[(fila, columna)]) - 1}"

        item = self.tableWidgetSemana.item(fila, columna)
        if item:
            item.setText(texto_celda)

            # Actualizar color según el estado
            if estado.lower() == "pendiente":
                item.setBackground(QBrush(QColor(255, 140, 0)))  # Naranja oscuro
            elif estado.lower() == "confirmada":
                item.setBackground(QBrush(QColor(0, 102, 204)))  # Azul oscuro
            item.setForeground(QBrush(QColor(255, 255, 255)))  # Texto blanco
            item.setTextAlignment(Qt.AlignCenter)

    def mostrarDetallesCita(self, fila, columna):
        clave_celda = (fila, columna)
        self.citas_actuales = self.citas_por_celda.get(clave_celda, [])
        self.indice_cita_actual = 0

        # Calcular fecha y hora de la celda seleccionada
        fecha = self.inicio_semana + timedelta(days=columna)
        horas = [
            "07:00:00", "08:00:00", "09:00:00", "10:00:00", "11:00:00",
            "12:00:00", "13:00:00", "14:00:00", "15:00:00", "16:00:00",
            "17:00:00", "18:00:00", "19:00:00"
        ]
        hora = datetime.strptime(horas[fila], "%H:%M:%S").time()

        # Actualizar dentistas disponibles
        self.cargarDentistasDisponibles(fecha, hora)

        if self.citas_actuales:
            self.actualizarPanelCita(self.citas_actuales[0])
        else:
            # Limpiar el panel y establecer fecha/hora
            self.dateEditFecha.setDate(fecha)
            self.timeEditHora.setTime(hora)
            self.limpiarPanel()

    def actualizarPanelCita(self, cita):
        fecha, hora, nombre_paciente, motivo, estado, dentista_asignado = cita
        hora_str = (datetime.min + hora).strftime("%H:%M:%S")

        # Establecer los valores en el panel
        if nombre_paciente not in [self.comboBoxPaciente.itemText(i) for i in range(self.comboBoxPaciente.count())]:
            self.comboBoxPaciente.addItem(nombre_paciente)
        self.comboBoxPaciente.setCurrentText(nombre_paciente)

        self.lineEditMotivo.setText(motivo)
        self.dateEditFecha.setDate(fecha)
        self.timeEditHora.setTime(datetime.strptime(hora_str, "%H:%M:%S").time())
        self.comboBoxEstado.setCurrentText(estado.capitalize())

        # Cargar dentistas disponibles para la fecha y hora
        try:
            conn = self.conectar_db()
            cursor = conn.cursor()
            
            query = """
                SELECT d.nombre
                FROM dentistas d
                WHERE d.id NOT IN (
                    SELECT c.id_dentista
                    FROM CitasMedicas c
                    WHERE c.fecha = %s AND c.hora = %s AND c.estado != 'cancelada'
                )
            """
            cursor.execute(query, (fecha, hora))
            dentistas_disponibles = cursor.fetchall()
            
            conn.close()

            # Actualizar el combo box con los dentistas disponibles y el asignado
            self.comboBoxDentista.clear()
            
            for dentista in dentistas_disponibles:
                self.comboBoxDentista.addItem(dentista[0])
            
            # Asegurar que el dentista asignado esté en la lista y seleccionado
            if dentista_asignado not in [self.comboBoxDentista.itemText(i) for i in range(self.comboBoxDentista.count())]:
                self.comboBoxDentista.addItem(dentista_asignado)
            self.comboBoxDentista.setCurrentText(dentista_asignado)

        except Exception as e:
            print(f"Error al cargar los dentistas disponibles: {e}")

    def limpiarPanel(self):
        self.comboBoxPaciente.setCurrentIndex(-1)  # No seleccionar ningún paciente
        self.lineEditMotivo.clear()
        self.dateEditFecha.clear()
        self.timeEditHora.clear()
        self.comboBoxEstado.setCurrentIndex(-1)
        self.comboBoxDentista.setCurrentIndex(-1)

    def mostrarCitaAnterior(self):
        if self.citas_actuales and self.indice_cita_actual > 0:
            self.indice_cita_actual -= 1
            cita_actual = self.citas_actuales[self.indice_cita_actual]
            self.actualizarPanelCita(cita_actual)
            fila, columna = self.obtenerCeldaDeCita(cita_actual)
            self.actualizarCeldaCita(fila, columna, cita_actual)

    def mostrarCitaSiguiente(self):
        if self.citas_actuales and self.indice_cita_actual < len(self.citas_actuales) - 1:
            self.indice_cita_actual += 1
            cita_actual = self.citas_actuales[self.indice_cita_actual]
            self.actualizarPanelCita(cita_actual)
            fila, columna = self.obtenerCeldaDeCita(cita_actual)
            self.actualizarCeldaCita(fila, columna, cita_actual)

    def obtenerCeldaDeCita(self, cita):
        fecha, hora = cita[0], cita[1]
        fecha_date = fecha if isinstance(fecha, date) else fecha.date()
        dia_semana = (fecha_date - self.inicio_semana).days

        hora_str = (datetime.min + hora).strftime("%H:%M:%S")
        hora_index = self.hora_a_indice(hora_str)

        return hora_index, dia_semana

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