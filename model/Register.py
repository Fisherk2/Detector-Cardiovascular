"""
============================================================
18/11/24
INTELIGENCIA ARTIFICIAL
Predictor de fulminación por paro cardiaco.

Equipo 8
Silva Pedraza Christian Ernesto
Villafaña Oliva César Omar
Zúñiga Gómez Jóse Alberto
============================================================
"""

import mariadb
from mariadb import Cursor
from config.Database import MariaDB

class Register():
    # ➤➤➤➤➤➤➤➤➤➤➤➤➤➤➤➤➤➤➤➤➤➤➤➤➤➤➤➤➤➤➤➤➤➤➤ ATRIBUTOS ➤➤➤➤➤➤➤➤➤➤➤➤➤➤➤➤➤➤➤➤➤➤➤➤➤➤➤➤➤➤➤➤➤➤➤ #
    DB: MariaDB = None
    CURSOR: Cursor = None
    USUARIO: str = ""
    PASSWORD: str = ""

    def __init__(self, user:str,pwd:str):
        """
        Clase modelo que consulta datos de la tabla donde se registran los usuarios de la base de datos.

        Args:
            user: Usuario de la base de datos
            pwd: Contraseña del usuario de la base de datos
        """
        self.DB = MariaDB(db="Cardiovascular")
        self.USUARIO = user
        self.PASSWORD = pwd

    def crear(self,
              id_usuario: int,
              sistolica: int,
              diastolica: int,
              colesterol: int,
              glucosa: int) -> bool:
        """
        Funcion que crea un registro por cada sensor cardiovascular.
        Args:
            id_usuario: ID del usuario
            sistolica: Presion Sistolica
            diastolica: Presion Diastolica
            colesterol: 1 = normal, 2 = arriba de lo normal, 3 = muy por encima de lo normal
            glucosa: 1 = normal, 2 = arriba de lo normal, 3 = muy por encima de lo normal

        Returns:
            Transaccion exitosa?
        """

        # ▬▬▬▬ Intentamos abrir la conexión a la base de datos ▬▬▬▬ #
        if not self.DB.conectar(usr=self.USUARIO, pwd=self.PASSWORD):
            return False

        # ▬▬▬▬ Creamos un cursor por cada conexion ▬▬▬▬ #
        self.CURSOR = self.DB.CONN.cursor()

        # ▬▬▬▬ Configuramos la consulta ▬▬▬▬ #
        query = """
            INSERT INTO register (id_usuario, ap_hi, ap_lo, cholesterol, gluc) 
            VALUES (?, ?, ?, ?, ?);
            """

        # ▬▬▬▬ Ejecutamos la consulta ▬▬▬▬ #
        try:
            self.CURSOR.execute(query, (id_usuario, sistolica, diastolica, colesterol, glucosa))
            self.DB.CONN.commit()
            return True
        except mariadb.Error as e:
            print(f"Error al crear usuario: {e}")
            self.DB.CONN.rollback()
            return False
        finally:
            self.DB.desconectar()

    def obtener(self, id_usuario: int) -> list:
        """
        Funcion que devuelve el contenido de la tabla donde solo se ven registros de un usuario especificado.
        Args:
            id_usuario: ID del usuario a consultar
        Returns:
            Lista de tuplas [()]

        """

        # ▬▬▬▬ Intentamos abrir la conexión a la base de datos ▬▬▬▬ #
        if not self.DB.conectar(usr=self.USUARIO, pwd=self.PASSWORD):
            return []

        # ▬▬▬▬ Creamos un cursor por cada conexion ▬▬▬▬ #
        self.CURSOR = self.DB.CONN.cursor()

        # ▬▬▬▬ Configuramos la consulta ▬▬▬▬ #
        query = """
                    SELECT * 
                    FROM register 
                    WHERE id_usuario = %s 
                    ORDER BY fecha DESC
                    LIMIT 10;
                """

        # ▬▬▬▬ Ejecutamos la consulta ▬▬▬▬ #
        try:
            self.CURSOR.execute(query, (id_usuario,))  # Usamos tupla para el parámetro
            resultados = self.CURSOR.fetchall()
            return resultados
        except mariadb.Error as e:
            print(f"Error al obtener la tabla: {e}")
            return []
        finally:
            self.DB.desconectar()

    def obtener_ultimo(self, id_usuario: int) -> dict:
        """
        Funcion que devuelve el ultimo registro de la tabla donde solo se ven registros de un usuario especificado.
        Args:
            id_usuario: ID del usuario a consultar
        Returns:
            Tupla () ó {} si esta vacio

        """

        # ▬▬▬▬ Intentamos abrir la conexión a la base de datos ▬▬▬▬ #
        if not self.DB.conectar(usr=self.USUARIO, pwd=self.PASSWORD):
            return {}

        # ▬▬▬▬ Creamos un cursor por cada conexion ▬▬▬▬ #
        self.CURSOR = self.DB.CONN.cursor()

        # ▬▬▬▬ Configuramos la consulta ▬▬▬▬ #
        query = """
            SELECT * 
            FROM register 
            WHERE id_usuario = %s 
            ORDER BY fecha DESC 
            LIMIT 1;
        """
        # ▬▬▬▬ Ejecutamos la consulta ▬▬▬▬ #
        try:
            self.CURSOR.execute(query, (id_usuario,))  # Usamos tupla para el parámetro
            resultado = self.CURSOR.fetchone()
            if resultado is None:
                #print(f"No se encontró el usuario con el ID {id_usuario}.")
                return {}
            return resultado
        except mariadb.Error as e:
            print(f"Error al obtener la tabla: {e}")
            return {}
        finally:
            self.DB.desconectar()


if __name__ == '__main__':
    tabla_registros = Register("registerCV","register123")
    # tabla_registros.crear(id_usuario=3, sistolica=120, diastolica=90, colesterol=1, glucosa=1)
    # print(tabla_registros.obtener_ultimo(id_usuario=1))
    for registro in tabla_registros.obtener(id_usuario=3):
        print(registro)
