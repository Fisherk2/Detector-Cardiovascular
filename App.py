"""
============================================================
21/11/24
INTELIGENCIA ARTIFICIAL
Predictor de fulminación por paro cardiaco.

Equipo 8
Silva Pedraza Christian Ernesto
Villafaña Oliva César Omar
Zúñiga Gómez Jóse Alberto
============================================================
"""
import threading
import time
import pandas as pd

from config.Fichero import Fichero
from model.Paciente import Contacto
from model.Predicter import Predicter
from model.Register import Register
from model.User import User
from view.Screen import Console
from viewmodel.Prompt import ViewModel
from viewmodel.Sensor import Sensor


class App():
    """
    Aplicacion de deteccion de complicaciones cardiovasculares.
    """

    # ➤➤➤➤➤➤➤➤➤➤➤➤➤➤➤➤➤➤➤➤➤➤➤➤➤➤➤➤➤➤➤➤➤➤➤ ATRIBUTOS ➤➤➤➤➤➤➤➤➤➤➤➤➤➤➤➤➤➤➤➤➤➤➤➤➤➤➤➤➤➤➤➤➤➤➤ #
    FILE: Fichero
    SAVE_FILE: dict
    PREDICT: Predicter
    REGISTROS: Register
    USUARIOS: User
    PACIENT: Contacto
    GUI: Console
    VIEWMODEL: ViewModel
    SENSOR: Sensor

    def __init__(self):
        # ▬▬▬▬ CARGAMOS DATOS GUARDADOS ▬▬▬▬ #
        self.FILE = Fichero()
        self.SAVE_FILE = self.FILE.cargar_json(file_path="config/save.json")

        # ▬▬▬▬ PREPARAMOS MODELO ▬▬▬▬ #
        self.PREDICT = Predicter(dataset=pd.read_csv(filepath_or_buffer="model/cardio_train.csv", sep=';'))
        self.PREDICT.entrenar_modelo(max_iter=100, test_size=0.3, ramdom_state=0)
        self.REGISTROS = Register(user="adminCV", pwd="admin123")
        self.USUARIOS = User(user="adminCV", pwd="admin123")
        self.PACIENT = Contacto(
            correo_electronico=self.SAVE_FILE["email"],
            telefono=self.SAVE_FILE["phone_number"],
            chat_id_telegram=self.SAVE_FILE["chat_id_telegram"]
        )

        # ▬▬▬▬ PREPARAMOS VISTA ▬▬▬▬ #
        self.GUI = Console()

        # ▬▬▬▬ PREPARAMOS CONTROLADOR ▬▬▬▬ #
        self.VIEWMODEL = ViewModel(
            predictor=self.PREDICT,
            usuarios=self.USUARIOS,
            registros=self.REGISTROS,
            vista=self.GUI
        )
        self.SENSOR = Sensor(predictor=self.PREDICT, tabla_usuarios=self.USUARIOS, tabla_registros=self.REGISTROS)

    def analisis_pulso(self):
        """
        Hilo que analiza las pulsaciones del usuario cada 10 segundos.
        """
        while True:
            # ▬▬▬▬ Cargamos el id de sesion cada que el sensor necesite analizar alguna muestra. ▬▬▬▬ #
            muestra: dict = self.SENSOR.lectura_pulso(
                id_usuario=self.FILE.cargar_json(file_path="config/save.json")["id_session"],
                sujeto=self.PACIENT
            )
            self.SENSOR.analizar_muestra(sujeto=self.PACIENT, muestra=muestra)

            # ▬▬▬▬ Volvera a analizar el pulso del usuario cada cierto tiempo ▬▬▬▬ #
            time.sleep(self.SAVE_FILE["pulse_timer"])

    def interfaz(self):
        """
        Hilo que muestra la interfaz al usuario para consulta de sus datos.
        """
        self.VIEWMODEL.iniciar()

    def run(self):
        # ▬▬▬▬ Instanciamos procesos de la aplicacion. ▬▬▬▬ #
        hilo_principal = threading.Thread(target=self.interfaz)
        hilo_secundario = threading.Thread(target=self.analisis_pulso, daemon=True)

        # ▬▬▬▬ Analizador de pulsos iniciara con un segundo de retraso ▬▬▬▬ #
        hilo_principal.start()
        time.sleep(1)
        hilo_secundario.start()

        # ▬▬▬▬ Esperamos a que el hilo de la interfaz termine ▬▬▬▬ #
        hilo_principal.join()

        # ▬▬▬▬ Cuando el hilo principal termine, los hilos demonios (como el de análisis de pulso) se detendrán automáticamente ▬▬▬▬ #
