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
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

class Gmail:
    """
    Clase que almacena la configuracion de correo electronico GMAIL y envia notificaciones a un buzon de correo.
    """

    # ➤➤➤➤➤➤➤➤➤➤➤➤➤➤➤➤➤➤➤➤➤➤➤➤➤➤➤➤➤➤➤➤➤➤➤ ATRIBUTOS ➤➤➤➤➤➤➤➤➤➤➤➤➤➤➤➤➤➤➤➤➤➤➤➤➤➤➤➤➤➤➤➤➤➤➤ #
    SENDER: str
    SENDER_NAME: str
    APP_PASSWORD: str
    SMPT: str
    PORT: int

    def __init__(self,
                 remitente: str,
                 contraseña_app: str,
                 smpt: str,
                 nombre_remitente: str = "Detector Cardiovascular",
                 port: int = 587):
        """
        Clase que almacena la configuracion de correo electronico GMAIL y envia notificaciones a un buzon de correo.
        Args:
            remitente: Dirección de correo electrónico del remitente.
            nombre_remitente: Nombre del remitente.
            contraseña_app: Contraseña del correo electronico del remitente
            smpt: Servidor SMTP de Gmail
            port: Puerto de envio a dicho servidor
        """
        self.SENDER = remitente
        self.SENDER_NAME = nombre_remitente
        self.APP_PASSWORD = contraseña_app
        self.SMPT = smpt
        self.PORT = port

    def enviar_mensaje(self, destinatario, asunto, cuerpo) -> bool:
        """
        Metodo que envia un correo electronico a un destinatario.
        Args:
            destinatario: Correo destino.
            asunto: Asunto del correo.
            cuerpo: Contenido del correo.

        Returns:
            ¿Correo enviado exitosamente?
        """

        # ▬▬▬▬ Construimos el mensaje ▬▬▬▬ #
        mensaje = MIMEMultipart()
        mensaje["From"] = self.SENDER_NAME
        mensaje["To"] = destinatario
        mensaje["Subject"] = asunto
        mensaje.attach(MIMEText(cuerpo, "plain"))

        # ▬▬▬▬ Intentamos conectarnos al servidor de correos GMAIL ▬▬▬▬ #
        try:
            with smtplib.SMTP(self.SMPT, self.PORT) as server:
                server.starttls()
                server.login(self.SENDER, self.APP_PASSWORD)
                server.sendmail(self.SENDER, destinatario, mensaje.as_string())
                #print("Correo enviado exitosamente.")
                return True
        except Exception as e:
            print(f"Error al enviar el correo: {e}")
            return False

if __name__ == '__main__':
    correo = Gmail(nombre_remitente="hanonimus")
    correo.enviar_mensaje(destinatario="jhoseline.vr99@gmail.com",asunto="Te vamos anexar",cuerpo="Te abrieron una carpeta de investigacion, deja jugar al Fish de tanque")

