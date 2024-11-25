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

from twilio.rest import Client


class TwilioSMS():
    # ➤➤➤➤➤➤➤➤➤➤➤➤➤➤➤➤➤➤➤➤➤➤➤➤➤➤➤➤➤➤➤➤➤➤➤ ATRIBUTOS ➤➤➤➤➤➤➤➤➤➤➤➤➤➤➤➤➤➤➤➤➤➤➤➤➤➤➤➤➤➤➤➤➤➤➤ #
    CLIENT: Client = None
    TWILIO_NUMBER:str

    def __init__(self,
                 twilio_numero_telefonico:str,
                 cuenta_SID: str,
                 token_auth: str):
        """
        Clase que almacena la configuracion para enviar SMS por medio de la API de Twilio.
        Args:
            twilio_numero_telefonico: Numero telefonico asignado por Twilio.
            cuenta_SID: Cuenta SID
            token_auth: Token de autorizacion que asigna Twilio a dicha cuenta SID.
        """
        self.CLIENT = Client(cuenta_SID, token_auth)
        self.TWILIO_NUMBER = twilio_numero_telefonico

    def enviar_sms(self, mensaje: str, numero_telefonico: str) -> bool:
        """
        Funcion que envia un SMS de alerta.
        Args:
            mensaje: Contenido del SMS
            numero_telefonico: Numero destinatario a enviar. (SOLO DE MEXICO +52)

        Returns:
            ¿Se envio el SMS?

        """

        # ▬▬▬▬ Intenta enviar SMS al telefono destino ▬▬▬▬ #
        try:
            message = self.CLIENT.messages.create(
                from_=self.TWILIO_NUMBER,
                body=mensaje,
                to='+52'+numero_telefonico
            )
            #print(f"Mensaje SMS enviado existosamente: {message.sid}")
            return True
        except Exception as e:
            print(f"No se ha podido enviar SMS: {e}")
            return False


if __name__ == '__main__':
    sms = TwilioSMS()

    sms.enviar_sms(
        mensaje="CUIDADO: puedes tener un paro cardiaco, ve al medico",
        numero_telefonico="5511865380"
    )
