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

import json
import os

class Fichero():
    """
    Clase que almacena las propiedades de un fichero.
    """

    def cargar_json(self, file_path: str) -> dict:
        """
        Carga el contenido de un archivo JSON en un diccionario.

        Args:
            file_path (str): Ruta al archivo JSON.

        Returns:
            dict: Diccionario con los datos del archivo JSON.

        Raises:
            FileNotFoundError: Si el archivo no existe.
            json.JSONDecodeError: Si el archivo no es un JSON válido.
        """
        # ▬▬▬▬ Validar si el archivo existe ▬▬▬▬ #
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"El archivo '{file_path}' no fue encontrado.")

        try:
            # ▬▬▬▬ Leer el archivo ▬▬▬▬ #
            with open(file_path, "r", encoding="utf-8") as archivo:
                return json.load(archivo)
        except json.JSONDecodeError as e:
            raise ValueError(f"Error al decodificar JSON en el archivo '{file_path}': {e}")

    def actualizar_json(self, file_path: str, clave: str, nuevo_valor):
        """
        Actualiza un elemento específico en un archivo JSON.

        Args:
            file_path (str): Ruta al archivo JSON.
            clave (str): Clave del elemento a actualizar.
            nuevo_valor: Nuevo valor a asignar a la clave.

        Raises:
            FileNotFoundError: Si el archivo no existe.
            json.JSONDecodeError: Si el archivo no es un JSON válido.
        """
        # ▬▬▬▬ Validar si el archivo existe ▬▬▬▬ #
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"El archivo '{file_path}' no fue encontrado.")

        try:
            # ▬▬▬▬ Leer el archivo y cargar datos ▬▬▬▬ #
            datos = self.cargar_json(file_path=file_path)

            # ▬▬▬▬ Actualizar el valor de la clave ▬▬▬▬ #
            if clave not in datos:
                raise KeyError(f"La clave '{clave}' no existe en el JSON.")
            datos[clave] = nuevo_valor

            # ▬▬▬▬ Escribir los datos actualizados en el archivo ▬▬▬▬ #
            with open(file_path, "w", encoding="utf-8") as archivo:
                json.dump(datos, archivo, indent=4, ensure_ascii=False)

        except json.JSONDecodeError as e:
            raise ValueError(f"Error al decodificar JSON en el archivo '{file_path}': {e}")


if __name__ == '__main__':
    archivo = Fichero()
    datos = archivo.cargar_json(file_path="keys.json")
    print(datos)

