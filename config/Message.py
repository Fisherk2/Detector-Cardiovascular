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

import requests

class Telegram:
    def __init__(self, chat_id: str, bot_token: str):
        self.CHAT_ID = chat_id
        self.API_URL = f"https://api.telegram.org/bot{bot_token}/sendMessage"

    def enviar_mensaje(self, mensaje):
        try:
            payload = {"chat_id": self.CHAT_ID, "text": mensaje}
            response = requests.post(self.API_URL, json=payload)
            if response.status_code != 200:
                print(f"Error al enviar el mensaje a Telegram: {response.text}")

            response.close()
        except Exception as e:
            print("Error, verifica tu bot token de la api o tu chat id de telegram: ", e)

if __name__ == '__main__':
    # wasa = Whatsapp()
    # wasa.enviar_mensaje_ahora(numero_telefonico="3310397940",mensaje="Holi")
    telegram = Telegram(chat_id="1211068213")
    telegram.enviar_mensaje("Hola")
