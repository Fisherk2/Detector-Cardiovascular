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
from mariadb import Connection

class MariaDB():
    """
    Clase que almacena configuraciones y conecta con base de datos de MariaDB.
    """

    # ➤➤➤➤➤➤➤➤➤➤➤➤➤➤➤➤➤➤➤➤➤➤➤➤➤➤➤➤➤➤➤➤➤➤➤ ATRIBUTOS ➤➤➤➤➤➤➤➤➤➤➤➤➤➤➤➤➤➤➤➤➤➤➤➤➤➤➤➤➤➤➤➤➤➤➤ #
    HOST: str
    PORT: int
    DB: str
    CONN: Connection = None

    def __init__(self, db: str, host: str = "localhost", port: int = 3306):
        """
        Clase que almacena configuraciones y conecta con base de datos de MariaDB.
        Args:
            db: Nombre de la base de datos
            host: Direccion del host de la base de datos.
            port: Numero de puerto de conexion a la base de datos.
        """
        self.HOST = host
        self.PORT = port
        self.DB = db

    def conectar(self, usr: str, pwd: str) -> bool:

        try:
            # ▬▬▬▬ Conectamos a la base de datos de MariaDB ▬▬▬▬ #
            self.CONN = mariadb.connect(
                user=usr,
                password=pwd,
                host=self.HOST,
                port=self.PORT,
                database=self.DB
            )
            #print("Conexión exitosa a la base de datos.")
            return True
        except mariadb.Error as e:
            print(f"Error conectando a MariaDB: {e}")
            return False
        except Exception as e:
            print(f"Error inesperado: {e}")
            return False

    def desconectar(self) -> bool:

        # ▬▬▬▬ Cerramos la base de datos de MariaDB ▬▬▬▬ #
        if self.CONN:
            try:
                self.CONN.close()
                return True
            except mariadb.Error as e:
                print(f"Error al intentar cerrar la conexión: {e}")
                return False
        else:
            print("No hay conexión activa para cerrar.")
            return False


if __name__ == '__main__':
    bd = MariaDB(db="Cardiovascular")
    bd.conectar(usr="registerCV", pwd="register123")
    bd.desconectar()
