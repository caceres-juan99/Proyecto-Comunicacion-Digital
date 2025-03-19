import sys    
import csv
import serial
import time
import datetime
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
import numpy as np
import pyqtgraph as pg
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QPushButton

class SerialPlot(QWidget):   ## Se declara una clase para el manejo del Widget

    def __init__(self, parent = None):              ### Función para configurar la ventana
        super(SerialPlot, self).__init__(parent)

        # Configuración de la ventana principal 
        self.setWindowTitle("Lanzamiento balón de baloncesto")
        self.setWindowState(Qt.WindowMaximized)    ### Utilizar la pantalla completa
        self.setGeometry(0, 0, 800, 600)

        # Configuración del gráfico de la aceleración 
        self.graphWidget = pg.PlotWidget(self)
        self.graphWidget.setGeometry(50, 50, 400, 350)
        self.graphWidget.setBackground('white')
        self.graphWidget.showGrid(x=True, y=True)
        self.graphWidget.setLabel('left', '<span style="color: black; font-size: 18px;">Magnitud</span>')
        self.graphWidget.setLabel('bottom', '<span style="color: black; font-size: 18px;">Tiempo (s)</span>')
        self.graphWidget.setLabel('top', '<span style="color: black; font-size: 18px;">Acelerometro</span>')
        self.graphWidget.getAxis('left').setStyle(tickFont=QFont('Times New Roman', 12))
        self.graphWidget.getAxis('bottom').setStyle(tickFont=QFont('Times New Roman', 12))
        self.graphWidget.getAxis('left').setPen(pg.mkPen(color='black'))  # Color del eje y
        self.graphWidget.getAxis('bottom').setPen(pg.mkPen(color='black'))  # Color del eje x
        self.graphWidget.getAxis('left').setGrid(True)  # Activa la cuadrícula en el eje y
        self.graphWidget.getAxis('bottom').setGrid(True)  # Activa la cuadrícula en el eje x
        
         # Configuración del gráfico del giroscopio 
        self.graphWidget2 = pg.PlotWidget(self)
        self.graphWidget2.setGeometry(500, 50, 400, 350)
        self.graphWidget2.setBackground('white')
        self.graphWidget2.showGrid(x=True, y=True)
        self.graphWidget2.setLabel('left', '<span style="color: black; font-size: 18px;">Magnitud</span>')
        self.graphWidget2.setLabel('bottom', '<span style="color: black; font-size: 18px;">Tiempo (s)</span>')
        self.graphWidget2.setLabel('top', '<span style="color: black; font-size: 18px;">Giroscopio</span>')
        self.graphWidget2.getAxis('left').setStyle(tickFont=QFont('Times New Roman', 12))
        self.graphWidget2.getAxis('bottom').setStyle(tickFont=QFont('Times New Roman', 12))
        self.graphWidget2.getAxis('left').setPen(pg.mkPen(color='black'))  # Color del eje y
        self.graphWidget2.getAxis('bottom').setPen(pg.mkPen(color='black'))  # Color del eje x
        self.graphWidget2.getAxis('left').setGrid(True)  # Activa la cuadrícula en el eje y
        self.graphWidget2.getAxis('bottom').setGrid(True)  # Activa la cuadrícula en el eje x
        
        # Configuración del gráfico de la Altura 
        self.graphWidget3 = pg.PlotWidget(self)
        self.graphWidget3.setGeometry(50, 450, 400, 350)
        self.graphWidget3.setBackground('white')
        self.graphWidget3.showGrid(x=True, y=True)
        self.graphWidget3.setLabel('left', '<span style="color: black; font-size: 18px;">Altitud (metros)</span>')
        self.graphWidget3.setLabel('bottom', '<span style="color: black; font-size: 18px;">Tiempo (s)</span>')
        self.graphWidget3.setLabel('top', '<span style="color: black; font-size: 18px;">Altura</span>')
        self.graphWidget3.getAxis('left').setStyle(tickFont=QFont('Times New Roman', 12))
        self.graphWidget3.getAxis('bottom').setStyle(tickFont=QFont('Times New Roman', 12))
        self.graphWidget3.getAxis('left').setPen(pg.mkPen(color='black'))  # Color del eje y
        self.graphWidget3.getAxis('bottom').setPen(pg.mkPen(color='black'))  # Color del eje x
        self.graphWidget3.getAxis('left').setGrid(True)  # Activa la cuadrícula en el eje y
        self.graphWidget3.getAxis('bottom').setGrid(True)  # Activa la cuadrícula en el eje x
        
        # Configuración del gráfico de la Temperatura
        self.graphWidget4 = pg.PlotWidget(self)
        self.graphWidget4.setGeometry(500, 450, 400, 350)
        self.graphWidget4.setBackground('white')
        self.graphWidget4.showGrid(x=True, y=True)
        self.graphWidget4.setLabel('left', '<span style="color: black; font-size: 18px;">°C</span>')
        self.graphWidget4.setLabel('bottom', '<span style="color: black; font-size: 18px;">Tiempo (s)</span>')
        self.graphWidget4.setLabel('top', '<span style="color: black; font-size: 18px;">Temperatura</span>')
        self.graphWidget4.getAxis('left').setStyle(tickFont=QFont('Times New Roman', 12))
        self.graphWidget4.getAxis('bottom').setStyle(tickFont=QFont('Times New Roman', 12))
        self.graphWidget4.getAxis('left').setPen(pg.mkPen(color='black'))  # Color del eje y
        self.graphWidget4.getAxis('bottom').setPen(pg.mkPen(color='black'))  # Color del eje x
        self.graphWidget4.getAxis('left').setGrid(True)  # Activa la cuadrícula en el eje y
        self.graphWidget4.getAxis('bottom').setGrid(True)  # Activa la cuadrícula en el eje x
        
        # Configuración del puerto serial
        self.ser = serial.Serial('COM4', 115200)
        self.ser.flush()

        # Variables para almacenar los datos
        num_points = 1000  # Número de puntos a mostrar en la gráfica
        self.x_data = np.zeros(num_points)    ## Tiempo
        self.y_data_1 = np.zeros(num_points)  # AcX
        self.y_data_2 = np.zeros(num_points)  # AcY
        self.y_data_3 = np.zeros(num_points)  # AcZ
        self.y_data_4 = np.zeros(num_points)  # GyX
        self.y_data_5 = np.zeros(num_points)  # GyY
        self.y_data_6 = np.zeros(num_points)  # GyZ
        self.y_data_7 = np.zeros(num_points)  # Altura
        self.y_data_8 = np.zeros(num_points)  # Temperatura
        self.start_time = time.time()

        # Crear las líneas para cada valor a graficar      
        pen_width = 2  # Ancho del trazo
        self.curve1 = self.graphWidget.plot(self.x_data, self.y_data_1, pen=pg.mkPen(color='r', width=pen_width), name='AcX')
        self.curve2 = self.graphWidget.plot(self.x_data, self.y_data_2, pen=pg.mkPen(color='g', width=pen_width), name='AcY')
        self.curve3 = self.graphWidget.plot(self.x_data, self.y_data_3, pen=pg.mkPen(color='b', width=pen_width), name='AcZ')
        self.curve4 = self.graphWidget2.plot(self.x_data, self.y_data_4, pen=pg.mkPen(color='r', width=pen_width), name='GyX')
        self.curve5 = self.graphWidget2.plot(self.x_data, self.y_data_5, pen=pg.mkPen(color='g', width=pen_width), name='GyY')
        self.curve6 = self.graphWidget2.plot(self.x_data, self.y_data_6, pen=pg.mkPen(color='b', width=pen_width), name='GyZ')
        self.curve7 = self.graphWidget3.plot(self.x_data, self.y_data_7, pen=pg.mkPen(color='orange', width=pen_width), name='Altura')
        self.curve8 = self.graphWidget4.plot(self.x_data, self.y_data_8, pen=pg.mkPen(color='black', width=pen_width), name='Temperatura')
        
        # Crear etiquetas
        self.pos_0_0 = QLabel(self)
        self.pos_0_1 = QLabel(self)
        self.pos_0_2 = QLabel(self)
        self.pos_2_0 = QLabel(self)
        self.pos_2_1 = QLabel(self)
        self.pos_2_2 = QLabel(self)
        
        
        # Configuración de la matriz de layouts
        layout_matrix = QGridLayout()
        self.setLayout(layout_matrix)

        # Añadir    las gráficas al layout
        layout_matrix.addWidget(self.graphWidget, 0, 0)  # Gráfica de aceleración
        layout_matrix.addWidget(self.graphWidget2, 0, 1)  # Gráfica de giroscopio
        layout_matrix.addWidget(self.graphWidget3, 1, 0)  # Gráfica de altura
        layout_matrix.addWidget(self.graphWidget4, 1, 1)  # Gráfica de temperatura

        # Configuración del diseño principal
        layout_main = QVBoxLayout()
        layout_main.addLayout(layout_matrix)
        self.setLayout(layout_main)
          
        # Configuración del temporizador para actualizar los datos
        self.timer = QTimer()
        self.timer.timeout.connect(self.update_data)
        self.timer.start(1)                #####    Número de muestras por segundo
        self.csv_header_written = False  # Inicializar la variable csv_header_written
 
    def update_data(self):
        # Leer los datos del puerto serie
        line = self.ser.readline().decode().strip()
        values = line.split(',')

        # Añadir los nuevos valores a los datos de la aceleración
        self.y_data_1[:-1] = self.y_data_1[1:]
        self.y_data_1[-1] = float(values[0])
        self.y_data_2[:-1] = self.y_data_2[1:]
        self.y_data_2[-1] = float(values[1])
        self.y_data_3[:-1] = self.y_data_3[1:]
        self.y_data_3[-1] = float(values[2])
        # Añadir los nuevos valores a los datos del giroscopio
        self.y_data_4[:-1] = self.y_data_4[1:]
        self.y_data_4[-1] = float(values[3])
        self.y_data_5[:-1] = self.y_data_5[1:]
        self.y_data_5[-1] = float(values[4])
        self.y_data_6[:-1] = self.y_data_6[1:]
        self.y_data_6[-1] = float(values[5])
        # Añadir los nuevos valores a los datos de la altura
        self.y_data_7[:-1] = self.y_data_7[1:]
        self.y_data_7[-1] = float(values[6])
        # Añadir los nuevos valores a los datos de la Temperatura
        self.y_data_8[:-1] = self.y_data_7[1:]
        self.y_data_8[-1] = float(values[7])
        # Crear valores para el tiempo
        self.x_data[:-1] = self.x_data[1:]
        elapsed_time = time.time() - self.start_time
        self.x_data[-1] = elapsed_time
        
        # Actualizar las líneas de la gráfica con los nuevos datos -> (Tiempo, Aceleración)
        self.curve1.setData(self.x_data, self.y_data_1)
        self.curve2.setData(self.x_data, self.y_data_2)
        self.curve3.setData(self.x_data, self.y_data_3)
        # Actualizar las líneas de la gráfica con los nuevos datos -> (Tiempo, Giroscopio)
        self.curve4.setData(self.x_data, self.y_data_4)
        self.curve5.setData(self.x_data, self.y_data_5)
        self.curve6.setData(self.x_data, self.y_data_6)
        # Actualizar las líneas de la gráfica con los nuevos datos -> (Tiempo, Altura)
        self.curve7.setData(self.x_data, self.y_data_7)
        # Actualizar las líneas de la gráfica con los nuevos datos -> (Tiempo, Temperatura)
        self.curve8.setData(self.x_data, self.y_data_8)

        # Guardar los nuevos datos en el archivo CSV
        if not self.csv_header_written:
            with open('Participante.csv', 'w', newline='') as archivo_csv:
                escritor_csv = csv.writer(archivo_csv)
                escritor_csv.writerow(['t (s)', 'AceX', 'AceY', 'AceZ', 'GirX', 'GirY', 'GirZ', 'Altura', 'Temperatura'])
            self.csv_header_written = True

        with open('Participante.csv', 'a', newline='') as archivo_csv:
            escritor_csv = csv.writer(archivo_csv)
            escritor_csv.writerow([self.x_data[-1], values[0], values[1], values[2], values[3], values[4], values[5], values[6], values[7]])

       
if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = SerialPlot()
    ex.show()
    sys.exit(app.exec_())
    