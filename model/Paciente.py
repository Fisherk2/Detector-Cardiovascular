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
from config.Fichero import Fichero
from config.Mail import Gmail
from config.Message import Telegram
from config.SMS import TwilioSMS
import random


class Contacto():
    """
    Clase que almacena los contactos del usuario dentro de la aplicacion.
    """

    # ➤➤➤➤➤➤➤➤➤➤➤➤➤➤➤➤➤➤➤➤➤➤➤➤➤➤➤➤➤➤➤➤➤➤➤ ATRIBUTOS ➤➤➤➤➤➤➤➤➤➤➤➤➤➤➤➤➤➤➤➤➤➤➤➤➤➤➤➤➤➤➤➤➤➤➤ #
    MAILER: Gmail = None
    SMS: TwilioSMS = None
    TELEGRAM: Telegram = None
    EMAIL: str
    PHONE: str

    def __init__(self, correo_electronico: str, telefono: str, chat_id_telegram: str):
        """
        Clase que almacena las propiedades del usuario dentro de la aplicacion.
        Args:
            correo_electronico: Correo electronico valido del usuario.
            telefono: Numero de telefono de Mexico (+52) del usuario.
            chat_id_telegram: ID del chat personal del Telegram del usuario.
        """
        # ▬▬▬▬ CARGAMOS CREDENCIALES DE MENSAJERIA ▬▬▬▬ #
        archivo = Fichero()
        credenciales: dict = archivo.cargar_json(file_path="config/keys.json")

        self.MAILER = Gmail(
            remitente=credenciales["email_sender"],
            smpt=credenciales["smpt"],
            contraseña_app=credenciales["pwd_app"]
        )

        self.SMS = TwilioSMS(
            twilio_numero_telefonico=credenciales["sms_sender"],
            cuenta_SID=credenciales["sid"],
            token_auth=credenciales["sid_auth"]
        )

        self.TELEGRAM = Telegram(
            chat_id=chat_id_telegram,
            bot_token=credenciales["bot_token_tg"]
        )

        self.EMAIL = correo_electronico
        self.PHONE = telefono

    def generar_registro_aleatorio(self) -> tuple[int, int, int, int]:
        """
        Metodo que registra un pulso del sujeto con valores aleatorios.
        Returns:
            Tupla [sistolica,diastolica,colesterol,glucosa]
        """
        sistolica = random.randint(60, 190)
        diastolica = random.randint(30, 120)

        # ▬▬▬▬ Diastolica no debe ser mayor a la sistolica ▬▬▬▬ #
        while (diastolica >= sistolica):
            diastolica = random.randint(30, 80)

        colesterol = random.randint(1, 3)
        glucosa = random.randint(1, 3)

        return sistolica, diastolica, colesterol, glucosa

    def mandar_msg(self,
                   nombre_usuario: str,
                   gravedad: int,
                   sistolica: int,
                   diastolica: int,
                   colesterol: int,
                   glucosa: int):
        """
        Enviamos mensaje de informacion al usuario dependiendo de la gravedad del su situacion cardiaca.
        Args:
            nombre_usuario: Nombre que se le tiene que enviar este mensaje.
            gravedad: Nivel de gravedad del asunto dependiendo de su salud cardiaca.
            sistolica: Presion Sistolica
            diastolica: Presion Diastolica
            colesterol: 1 = normal, 2 = arriba de lo normal, 3 = muy por encima de lo normal
            glucosa: 1 = normal, 2 = arriba de lo normal, 3 = muy por encima de lo normal
        """
        # ▬▬▬▬ Enviamos un mensaje por consola para advertir al usuario que esta en peligro. ▬▬▬▬ #
        print("\n⚠️ ALERTA ⚠️")
        print("Se ha detectado una anomalía en su sistema cardiovascular.")
        print("\n>>>>>>>>>>>>>>>>> ")

        # ▬▬▬▬ Seleccionamos uno o varios servicios de mensajeria dependiendo de la situacion. ▬▬▬▬ #
        match gravedad:
            case 1:
                mensaje = f"""
                                    ⚠️ ¡Advertencia de salud cardíaca! ⚠️  
                                    Su último registro indica irregularidades leves:  
                                    - Sistólica: {sistolica} mmHg  
                                    - Diastólica: {diastolica} mmHg  
                                    - Colesterol: {colesterol}  
                                    - Glucosa: {glucosa}
    
                                    Por favor, realice un chequeo médico preventivo.  
                                    - Detector Cardiovascular  
                    """
                self.TELEGRAM.enviar_mensaje(mensaje=mensaje)
            case 2:
                mensaje = f"""
                                    🚨 ¡ALERTA DE SALUD CARDÍACA! 🚨
                                    Hemos detectado irregularidades significativas:   
                                    - Sistólica: {sistolica} mmHg  
                                    - Diastólica: {diastolica} mmHg  
                                    - Colesterol: {colesterol}  
                                    - Glucosa: {glucosa}
    
                                    ⚠️ Consulte a su médico urgentemente. Más detalles enviados por correo.   
                                    - Detector Cardiovascular  
                                    """
                cuerpo = f"""
                                    Estimado(a) {nombre_usuario}:  
    
                                    Hemos analizado sus datos recientes y detectado irregularidades significativas que podrían representar un riesgo moderado para su salud.  
    
                                    ### Niveles detectados:  
                                    - **Presión sistólica:** {sistolica} mmHg  
                                    - **Presión diastólica:** {diastolica} mmHg  
                                    - **Colesterol:** {colesterol} 
                                    - **Glucosa:** {glucosa}  
    
                                    Estas cifras se encuentran fuera del rango saludable.  
    
                                    #### Recomendaciones:  
                                    1. Consulte a un médico lo antes posible para realizar exámenes adicionales.  
                                    2. Evite esfuerzos físicos intensos hasta tener una evaluación médica.  
                                    3. Lleve un control diario de sus síntomas.  
    
                                    ⚠️ Este mensaje es preventivo y no sustituye el diagnóstico de un profesional de la salud.  
    
                                    Saludos cordiales,  
                                    **Detector Cardiovascular Contra Paro Cardíaco**  
                    """
                self.TELEGRAM.enviar_mensaje(mensaje=mensaje)
                self.MAILER.enviar_mensaje(
                    destinatario=self.EMAIL,
                    asunto="⚠️ Alerta Importante de Salud Cardíaca ⚠️",
                    cuerpo=cuerpo
                )
            case 3:
                mensaje = f"""
                                    🚨🚨 ¡EMERGENCIA CARDÍACA DETECTADA! 🚨🚨  
                                    Sus datos recientes indican niveles críticos:  
                                    - Sistólica: {sistolica} mmHg  
                                    - Diastólica: {diastolica} mmHg  
                                    - Colesterol: {colesterol} 
                                    - Glucosa: {glucosa} 
    
                                    ⚠️ Contacte a emergencias médicas de inmediato. Más información en su correo y SMS.  
                                    - Detector Cardiovascular    
                                """
                cuerpo = f"""
                                    Estimado(a) {nombre_usuario}:  
    
                                    **URGENTE**: Hemos detectado indicadores críticos en su último análisis cardiovascular que requieren atención inmediata.  
    
                                    ### Niveles detectados:  
                                    - **Presión sistólica:** {sistolica} mmHg  
                                    - **Presión diastólica:** {diastolica} mmHg  
                                    - **Colesterol:** {colesterol}  
                                    - **Glucosa:** {glucosa}
    
                                    #### Recomendaciones urgentes:  
                                    1. Llame al servicio de emergencias médicas de inmediato (911 o equivalente local).  
                                    2. Evite actividades físicas o situaciones de estrés.  
                                    3. Asegúrese de estar acompañado por alguien que pueda asistirle.  
    
                                    ⚠️ Este mensaje no reemplaza el diagnóstico médico profesional.  
    
                                    Saludos cordiales,  
                                    **Detector Cardiovascular Contra Paro Cardíaco**  
    
                                """
                sms = f"""
                                    🚨 CRÍTICO 🚨  
                                    Sist.: {sistolica}, Diast.: {diastolica}, Coles.: {colesterol}, Glu.: {glucosa}.  
                                    Llame a emergencias.  
                                """
                self.TELEGRAM.enviar_mensaje(mensaje=mensaje)
                self.MAILER.enviar_mensaje(
                    destinatario=self.EMAIL,
                    asunto="🚨 Alerta Crítica de Salud Cardíaca 🚨️",
                    cuerpo=cuerpo
                )
                self.SMS.enviar_sms(mensaje=sms, numero_telefonico=self.PHONE)
