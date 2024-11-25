"""
============================================================
19/11/24
INTELIGENCIA ARTIFICIAL
Predictor de fulminación por paro cardiaco.

Equipo 8
Silva Pedraza Christian Ernesto
Villafaña Oliva César Omar
Zúñiga Gómez Jóse Alberto
============================================================
"""
import pandas as pd
from pandas import DataFrame

from model.Paciente import Contacto
from model.Register import Register
from model.Predicter import Predicter
from model.User import User

class Sensor():
    # ➤➤➤➤➤➤➤➤➤➤➤➤➤➤➤➤➤➤➤➤➤➤➤➤➤➤➤➤➤➤➤➤➤➤➤ ATRIBUTOS ➤➤➤➤➤➤➤➤➤➤➤➤➤➤➤➤➤➤➤➤➤➤➤➤➤➤➤➤➤➤➤➤➤➤➤ #
    TABLA_REGISTROS: Register
    TABLA_USUARIOS: User
    PREDICTER: Predicter = None

    def __init__(self, predictor: Predicter, tabla_registros: Register, tabla_usuarios: User):
        self.TABLA_USUARIOS = tabla_usuarios
        self.TABLA_REGISTROS = tabla_registros
        self.PREDICTER = predictor

    def lectura_pulso(self, id_usuario: int, sujeto: Contacto) -> dict:
        """
        Funcion que manda lectura de pulso del usuario y registra dicho pulso a la base de datos.
        Args:
            sujeto: Usuario sometido a una lectura cardiovascular.

        Returns:
            Diccionario de todos los datos del usuario obtenidos por dicha lectura.
        """

        # ▬▬▬▬ Verificamos si dicho usuario existe en la base de datos ▬▬▬▬ #
        if self.TABLA_USUARIOS.obtener_registro(id_usuario=id_usuario) == {}:
            return {}

        # ▬▬▬▬ Obtenemos datos biometricos del usuario ▬▬▬▬ #
        sistolica, diastolica, colesterol, glucosa = sujeto.generar_registro_aleatorio()

        # ▬▬▬▬ Enviar registro a la base de datos ▬▬▬▬ #
        self.TABLA_REGISTROS.crear(
            id_usuario=id_usuario,
            sistolica=sistolica,
            diastolica=diastolica,
            colesterol=colesterol,
            glucosa=glucosa
        )

        # ▬▬▬▬ Empaquetamos dichos datos para su analisis ▬▬▬▬ #
        id, name, age, gender, height, weight, smoke, alco, active = self.TABLA_USUARIOS.obtener_registro(
            id_usuario=id_usuario)

        datos_sujeto: dict = {
            "id": [id_usuario],
            "name": [name],
            "age": [age],  # Dias (27 años)
            "gender": [self.convertir_a_enteros(gender)],  # Genera numero hexadecimal
            "height": [height],  # cm
            "weight": [weight],  # kg
            "ap_hi": [sistolica],
            "ap_lo": [diastolica],
            "cholesterol": [colesterol],
            "gluc": [glucosa],
            "smoke": [self.convertir_a_enteros(smoke)],
            "alco": [self.convertir_a_enteros(alco)],
            "active": [self.convertir_a_enteros(active)]
        }

        return datos_sujeto

    def analizar_muestra(self, sujeto: Contacto, muestra: dict):

        # ▬▬▬▬ Rechazar analisis en caso de no encontrar muestras. ▬▬▬▬ #
        if muestra == {}:
            return

        # ▬▬▬▬ Generamos predicciones y coeficientes de morir por un problema cardiaco. ▬▬▬▬ #
        df = DataFrame(data=muestra)
        df = df.drop(columns="name", axis=1)

        prediccion, probabilidad_no_morir, probabilidad_morir = self.PREDICTER.predecir_registro(registro=df)

        # ▬▬▬▬ Enviamos una alerta en caso de peligro por problemas cardiovasculares ▬▬▬▬ #
        if prediccion != 0:

            niveles = [
                (1, 0.50 < probabilidad_morir <= 0.70),
                (2, 0.70 < probabilidad_morir <= 0.90),
                (3, probabilidad_morir > 0.90)
            ]

            # ▬▬▬▬ Dependiendo de la situacion, se le enviara un mensaje al usuario ▬▬▬▬ #
            for gravedad, condicion in niveles:
                if condicion:
                    sujeto.mandar_msg(
                        nombre_usuario=muestra["name"][0],
                        sistolica=muestra["ap_hi"][0],
                        diastolica=muestra["ap_lo"][0],
                        colesterol=muestra["cholesterol"][0],
                        glucosa=muestra["gluc"][0],
                        gravedad=gravedad
                    )
                    break

    def convertir_a_enteros(self, valor_byte: bytes) -> int:
        """
        Funcion que convierte cualquier valor de bytes en enteros.
        Args:
            valor_byte: Valor que esta en bytes

        Returns:
            Valor entero.
        """
        return int.from_bytes(valor_byte, byteorder='big') if isinstance(valor_byte, bytes) else valor_byte


if __name__ == '__main__':
    dataset = pd.read_csv(filepath_or_buffer="../model/cardio_train.csv", sep=';')
    predict = Predicter(dataset=dataset)
    predict.entrenar_modelo(max_iter=100, test_size=0.3, ramdom_state=0)
    tabla_registro = Register(user="registerCV", pwd="register123")
    tabla_usuarios = User(user="userCV", pwd="user123")

    usuario = Contacto(
        correo_electronico="20240641@leon.tecnm.mx",
        telefono="5511865380",
        chat_id_telegram="1211068213"
    )

    sensor = Sensor(predictor=predict, tabla_usuarios=tabla_usuarios, tabla_registros=tabla_registro)

    muestra = sensor.lectura_pulso(id_usuario=7, sujeto=usuario)
    sensor.analizar_muestra(sujeto=usuario, muestra=muestra)
