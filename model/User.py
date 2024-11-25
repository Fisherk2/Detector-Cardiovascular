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


class User():
    """
    Clase modelo que consulta datos de la tabla donde se registran los usuarios de la base de datos.
    """

    # ➤➤➤➤➤➤➤➤➤➤➤➤➤➤➤➤➤➤➤➤➤➤➤➤➤➤➤➤➤➤➤➤➤➤➤ ATRIBUTOS ➤➤➤➤➤➤➤➤➤➤➤➤➤➤➤➤➤➤➤➤➤➤➤➤➤➤➤➤➤➤➤➤➤➤➤ #
    DB: MariaDB = None
    CURSOR: Cursor = None
    USUARIO: str = ""
    PASSWORD: str = ""

    def __init__(self, user: str, pwd: str):
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
              nombre: str,
              edad: int,
              genero: int,
              altura: int,
              peso: int,
              fuma: bool,
              alcohol: bool,
              fis_activo: bool) -> bool:
        """
        Clase que crea un registro para la tabla de usuarios.
        Args:
            nombre: Nombre del usuario
            edad: En dias.
            genero: 1 = Femenino, 2 = Masculino
            altura: En Centimetros
            peso: En Kilogramos
            fuma: Fuma o no?
            alcohol: Es alcoholico o no?
            fis_activo: Es fisicamente activo?

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
            INSERT INTO usuario (name, age, gender, height, weight, smoke, alco, active)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s);
            """

        # ▬▬▬▬ Ejecutamos la consulta ▬▬▬▬ #
        try:
            self.CURSOR.execute(query, (nombre, edad, genero, altura, peso, int(fuma), int(alcohol), int(fis_activo)))
            self.DB.CONN.commit()
            # print(f"Usuario {nombre} creado con éxito.")
            return True
        except mariadb.Error as e:
            print(f"Error al crear usuario: {e}")
            self.DB.CONN.rollback()
            return False
        finally:
            self.DB.desconectar()

    def actualizar(self,
                   id: int,
                   nombre: str,
                   edad: int,
                   genero: int,
                   altura: int,
                   peso: int,
                   fuma: bool,
                   alcohol: bool,
                   fis_activo: bool) -> bool:
        """
        Funcion que permite actualizar todos los datos de algun registro de la tabla de usuarios registrados.
        Args:
            id: ID numerico que pertenece al usuario
            nombre: Nombre del usuario
            edad: En dias.
            genero: 1 = Femenino, 2 = Masculino
            altura: En Centimetros
            peso: En Kilogramos
            fuma: Fuma o no?
            alcohol: Es alcoholico o no?
            fis_activo: Es fisicamente activo?

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
            UPDATE usuario
            SET name = %s, age = %s, gender = %s, height = %s, weight = %s, smoke = %s, alco = %s, active = %s
            WHERE id = %s;
            """

        # ▬▬▬▬ Ejecutamos la consulta ▬▬▬▬ #
        try:
            self.CURSOR.execute(query, (
                nombre,
                edad,
                genero,
                altura,
                peso,
                int(fuma),
                int(alcohol),
                int(fis_activo),
                id
            ))
            self.DB.CONN.commit()
            # print(f"Usuario con ID {id} actualizado con éxito.")
            return True
        except mariadb.Error as e:
            print(f"Error al crear usuario: {e}")
            self.DB.CONN.rollback()
            return False
        finally:
            self.DB.desconectar()

    def eliminar(self, id: int) -> bool:
        """
        Funcion que elimina un registro de la tabla de usuarios registrados.
        Args:
            id: ID numerico que pertenece al usuario.

        Returns:
            Transaccion exitosa?
        """

        # ▬▬▬▬ Intentamos abrir la conexión a la base de datos ▬▬▬▬ #
        if not self.DB.conectar(usr=self.USUARIO, pwd=self.PASSWORD):
            return False

        # ▬▬▬▬ Creamos un cursor por cada conexion ▬▬▬▬ #
        self.CURSOR = self.DB.CONN.cursor()

        # ▬▬▬▬ Configuramos la consulta ▬▬▬▬ #
        query = "DELETE FROM usuario WHERE id = %s;"

        # ▬▬▬▬ Ejecutamos la consulta ▬▬▬▬ #
        try:
            self.CURSOR.execute(query, (id,))  # Usamos tupla para el parámetro
            self.DB.CONN.commit()
            # print(f"Usuario con ID {id} eliminado con éxito.")
            return True
        except mariadb.Error as e:
            print(f"Error al eliminar usuario: {e}")
            self.DB.CONN.rollback()
            return False
        finally:
            self.DB.desconectar()

    def obtener(self) -> list:
        """
        Funcion que devuelve el contenido completo de la tabla.
        Returns:
            Lista con todos los elementos de la tabla.
        """

        # ▬▬▬▬ Intentamos abrir la conexión a la base de datos ▬▬▬▬ #
        if not self.DB.conectar(usr=self.USUARIO, pwd=self.PASSWORD):
            return []

        # ▬▬▬▬ Creamos un cursor por cada conexion ▬▬▬▬ #
        self.CURSOR = self.DB.CONN.cursor()

        # ▬▬▬▬ Configuramos la consulta ▬▬▬▬ #
        query = "SELECT * FROM usuario;"

        # ▬▬▬▬ Ejecutamos la consulta ▬▬▬▬ #
        try:
            self.CURSOR.execute(query)
            resultados = self.CURSOR.fetchall()
            return resultados
        except mariadb.Error as e:
            print(f"Error al obtener la tabla: {e}")
            return []
        finally:
            self.DB.desconectar()

    def obtener_registro(self, id_usuario: int) -> dict:

        # ▬▬▬▬ Intentamos abrir la conexión a la base de datos ▬▬▬▬ #
        if not self.DB.conectar(usr=self.USUARIO, pwd=self.PASSWORD):
            return {}

        # ▬▬▬▬ Creamos un cursor por cada conexion ▬▬▬▬ #
        self.CURSOR = self.DB.CONN.cursor()

        # ▬▬▬▬ Configuramos la consulta ▬▬▬▬ #
        query = """
                    SELECT * 
                    FROM usuario 
                    WHERE id = %s 
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

    def obtener_ultimo_registro(self) -> dict:
        """
        Funcion que devuelve el ultimo usuario registrado en la base de datos.
        Returns:
            Tupla de valores con todos los campos de la tabla.
        """

        # ▬▬▬▬ Intentamos abrir la conexión a la base de datos ▬▬▬▬ #
        if not self.DB.conectar(usr=self.USUARIO, pwd=self.PASSWORD):
            return {}

        # ▬▬▬▬ Creamos un cursor por cada conexion ▬▬▬▬ #
        self.CURSOR = self.DB.CONN.cursor()

        # ▬▬▬▬ Configuramos la consulta ▬▬▬▬ #
        query = """
                    SELECT * 
                    FROM usuario 
                    ORDER BY id DESC 
                    LIMIT 1;
                """

        # ▬▬▬▬ Ejecutamos la consulta ▬▬▬▬ #
        try:
            self.CURSOR.execute(query)
            resultado = self.CURSOR.fetchone()
            if resultado is None:
                #print(f"No hay usuarios registrados.")
                return {}
            return resultado
        except mariadb.Error as e:
            print(f"Error al obtener la tabla: {e}")
            return {}
        finally:
            self.DB.desconectar()

if __name__ == '__main__':
    tabla_usuario = User(user="adminCV", pwd="admin123")
    tabla_usuario.eliminar(id=3)
    #print(tabla_usuario.obtener_registro(id_usuario=1))
    #print(tabla_usuario.obtener_ultimo_registro())
    """
    tabla_usuario.crear(
        nombre="Alessandro",
        edad=9496,
        genero=2,
        altura=173,
        peso=74,
        fuma=False,
        alcohol=True,
        fis_activo=True
    )
    """
    """
    tabla_usuario.actualizar(
        id=2,
        nombre="Alessandro",
        edad=9496,
        genero=2,
        altura=173,
        peso=74,
        fuma=False,
        alcohol=True,
        fis_activo=True
    )

    tabla_usuario.eliminar(id=2)
    """

    for usuario in tabla_usuario.obtener():
        print(usuario)
