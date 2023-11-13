import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel, QPushButton, QWidget, QVBoxLayout, QGridLayout
from PyQt5.QtGui import QImage, QPixmap, QIcon
from PyQt5.QtCore import Qt, QSize
import random

class JuegoCartas:
    def __init__(self):
        self.puntuacion_jugador1 = 0
        self.puntuacion_jugador2 = 0
        self.turno_jugador1 = True
        self.cartas_jugadas = 0
        self.max_cartas = 8

        self.valores_cartas = {
            "carta1.png": 50,
            "carta2.png": 150,
            "carta3.png": 350,
            "carta4.png": 500,
            "carta5.png": 50,
            "carta6.png": 50,
            "carta7.png": 500,
            "carta8.png": 150,
        }

    def hacer_clic_carta(self, nombre_carta):
        puntuacion_carta = self.valores_cartas.get(nombre_carta, 0)

        if self.turno_jugador1:
            self.puntuacion_jugador1 += puntuacion_carta
        else:
            self.puntuacion_jugador2 += puntuacion_carta

        self.turno_jugador1 = not self.turno_jugador1
        self.cartas_jugadas += 1

    def resetear_juego(self):
        self.puntuacion_jugador1 = 0
        self.puntuacion_jugador2 = 0
        self.turno_jugador1 = True
        self.cartas_jugadas = 0

class VentanaPrincipal(QMainWindow):
    def __init__(self):
        super().__init__()

        self.juego = JuegoCartas()
        self.inicializar_ui()

    def inicializar_ui(self):
        self.setGeometry(100, 100, 800, 533)
        self.setWindowTitle("PUÑOGRANADA")
        self.setFixedSize(800, 533)

        widget_inicial = QWidget()
        layout_inicial = QVBoxLayout()

        imagen_granada = QImage("granada.png")
        imagen_granada = imagen_granada.scaled(400, 400)
        pixmap_granada = QPixmap.fromImage(imagen_granada)

        etiqueta_granada = QLabel()
        etiqueta_granada.setPixmap(pixmap_granada)
        etiqueta_granada.setAlignment(Qt.AlignCenter)

        imagen_jugar = QImage("boton_jugar.png")
        imagen_jugar = imagen_jugar.scaled(200, 100)
        pixmap_jugar = QPixmap.fromImage(imagen_jugar)

        etiqueta_jugar = QLabel()
        etiqueta_jugar.setPixmap(pixmap_jugar)
        etiqueta_jugar.setAlignment(Qt.AlignCenter)

        layout_inicial.addWidget(etiqueta_granada)
        layout_inicial.addWidget(etiqueta_jugar)
        widget_inicial.setLayout(layout_inicial)

        self.widget_juego = QWidget()
        self.layout_juego = QVBoxLayout()

        self.etiqueta_turno = QLabel()
        self.layout_juego.addWidget(self.etiqueta_turno)

        self.botones = []

        self.setCentralWidget(widget_inicial)

        etiqueta_jugar.mousePressEvent = lambda event: self.mostrar_juego()

        self.setStyleSheet(
            "QMainWindow { background-image: url('fondo_puño_general.png'); background-repeat: repeat; background-position: center; }")

        self.show()

    def mostrar_juego(self):
        self.juego.resetear_juego()
        self.limpiar_y_crear_botones()
        self.actualizar_turno()
        self.setCentralWidget(self.widget_juego)

    def hacer_clic_carta(self, nombre_carta, boton):
        self.juego.hacer_clic_carta(nombre_carta)
        pixmap_carta = QPixmap(nombre_carta)
        boton.setIcon(QIcon(pixmap_carta))
        boton.setIconSize(pixmap_carta.size())
        boton.setEnabled(False)

        if self.juego.puntuacion_jugador1 >= 1000 or self.juego.puntuacion_jugador2 >= 1000 or \
                (self.juego.cartas_jugadas == self.juego.max_cartas and
                 self.juego.puntuacion_jugador1 < 1000 and
                 self.juego.puntuacion_jugador2 < 1000):
            self.mostrar_resultado()

        print(f"Puntuación Jugador 1: {self.juego.puntuacion_jugador1}, Puntuación Jugador 2: {self.juego.puntuacion_jugador2}")
        self.actualizar_turno()

    def mostrar_resultado(self):
        if self.juego.puntuacion_jugador1 >= 1000:
            imagen_resultado = QImage("jugador1gano.png")
            imagen_resultado = imagen_resultado.scaled(700, 150)
        elif self.juego.puntuacion_jugador2 >= 1000:
            imagen_resultado = QImage("jugador2gano.png")
            imagen_resultado = imagen_resultado.scaled(700, 150)
        else:
            imagen_resultado = QImage("empate.png")
            imagen_resultado = imagen_resultado.scaled(400, 150)

        pixmap_resultado = QPixmap.fromImage(imagen_resultado)

        etiqueta_resultado = QLabel()
        etiqueta_resultado.setPixmap(pixmap_resultado)
        etiqueta_resultado.setAlignment(Qt.AlignCenter)

        widget_resultado = QWidget()
        layout_resultado = QVBoxLayout()
        layout_resultado.addWidget(etiqueta_resultado)
        widget_resultado.setLayout(layout_resultado)

        self.setCentralWidget(widget_resultado)

    def actualizar_turno(self):
        if self.juego.turno_jugador1:
            imagen_jugador = QImage("jugador2.png")
        else:
            imagen_jugador = QImage("jugador1.png")

        imagen_jugador = imagen_jugador.scaled(300, 110)
        pixmap_jugador = QPixmap.fromImage(imagen_jugador)

        self.etiqueta_turno.setPixmap(pixmap_jugador)
        self.etiqueta_turno.setAlignment(Qt.AlignCenter)

    def limpiar_y_crear_botones(self):
        for boton in self.botones:
            boton.deleteLater()

        self.botones.clear()

        grid_layout = QGridLayout()

        nombres_cartas = list(self.juego.valores_cartas.keys())
        random.shuffle(nombres_cartas)

        for i, nombre_carta in enumerate(nombres_cartas):
            imagen_carta = QImage("carta_atras.png")
            imagen_carta = imagen_carta.scaled(140, 200)
            pixmap_carta = QPixmap.fromImage(imagen_carta)

            boton = QPushButton()
            boton.setIcon(QIcon(pixmap_carta))
            boton.setIconSize(QSize(140, 200))
            boton.setFixedSize(QSize(140, 200))
            boton.setStyleSheet("background-color: transparent; border: none;")
            boton.clicked.connect(lambda _, nombre=nombre_carta, b=boton: self.hacer_clic_carta(nombre, b))

            self.botones.append(boton)

            grid_layout.addWidget(boton, i // 4, i % 4)

        self.layout_juego.addLayout(grid_layout)
        self.widget_juego.setLayout(self.layout_juego)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    ventana = VentanaPrincipal()
    sys.exit(app.exec_())
