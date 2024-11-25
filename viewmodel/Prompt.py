"""
============================================================
20/11/24
INTELIGENCIA ARTIFICIAL
Predictor de fulminación por paro cardiaco.

Equipo 8
Silva Pedraza Christian Ernesto
Villafaña Oliva César Omar
Zúñiga Gómez Jóse Alberto
============================================================
"""
import math

import pandas as pd

from config.Fichero import Fichero
from model.Predicter import Predicter
from model.Register import Register
from model.User import User
from view.Screen import Console


class ViewModel():
    # ➤➤➤➤➤➤➤➤➤➤➤➤➤➤➤➤➤➤➤➤➤➤➤➤➤➤➤➤➤➤➤➤➤➤➤ ATRIBUTOS ➤➤➤➤➤➤➤➤➤➤➤➤➤➤➤➤➤➤➤➤➤➤➤➤➤➤➤➤➤➤➤➤➤➤➤ #
    FILE: Fichero
    PATH_SAVE_FILE: str = "config/save.json"
    TABLA_REGISTROS: Register
    TABLA_USUARIOS: User
    PREDICTER: Predicter = None
    VIEW: Console
    ID_USER: int

    def __init__(self,
                 predictor: Predicter,
                 registros: Register,
                 usuarios: User,
                 vista):
        """
        Clase que maneja la vista y el modelo dependiendo de los comando ingresados por el usuario.
        Args:
            predictor: Modelo de prediccion cardiovascular.
            registros: Tabla de registros de la base de datos.
            usuarios: Tabla de usuarios de la base de datos.
            vista: Vista o GUI para el usuario.
        """
        self.VIEW = vista
        self.PREDICTER = predictor
        self.TABLA_USUARIOS = usuarios
        self.TABLA_REGISTROS = registros

        # ▬▬▬▬ CARGAMOS DATOS GUARDADOS ▬▬▬▬ #
        self.FILE = Fichero()
        self.ID_USER = self.FILE.cargar_json(file_path=self.PATH_SAVE_FILE)["id_session"]

    def obtener_nombre(self) -> str:
        """
        Funcion que extrae el nombre del usuario de la sesion iniciada de la base de datos.
        Returns:
            Nombre del usuario.
        """
        return self.TABLA_USUARIOS.obtener_registro(id_usuario=self.ID_USER)[1]

    def convertir_a_enteros(self, valor_byte: bytes) -> int:
        """
        Funcion que convierte cualquier valor de bytes en enteros.
        Args:
            valor_byte: Valor que esta en bytes

        Returns:
            Valor entero.
        """
        return int.from_bytes(valor_byte, byteorder='big') if isinstance(valor_byte, bytes) else valor_byte

    def convertir_days_years(self, dias: int) -> int:
        """
        Conversion de dias a años.
        Args:
            dias: Numero de dias

        Returns:
            Años (contando bisiestos)
        """
        return math.floor(dias / 365.2425)

    def convertir_years_days(self, years: int) -> int:
        """
        Conversion de años a dias.
        Args:
            years: Numero de años

        Returns:
            Numero de dias transcurridos.
        """
        return math.floor(years * 365.2425) + 1  # Ya que redondea hacia abajo, quitando años en el proceso.

    def mostrar_inputs_usuario(self) -> tuple[str, int, int, int, int, bool, bool, bool]:
        """
        Funcion que devuelve valores generados por el usuario para la tabla de usuarios.
        Returns:
            nombre, edad_dias, genero, altura, peso, fuma, alcohol, activo
        """
        nombre: str = input("Ingrese su nombre >> ")

        edad: int = self.obtener_entrada(
            mensaje="Ingrese su edad [1-130] >> ",
            tipo=int,
            rango=(1, 130)
        )

        edad_dias: int = self.convertir_years_days(years=edad)

        genero: int = self.obtener_entrada(
            mensaje="Ingrese su género [1 = Femenino, 2 = Masculino] >> ",
            tipo=int,
            opciones=[1, 2]
        )

        altura: int = self.obtener_entrada(
            mensaje="Ingrese su altura en centímetros [60-275] >> ",
            tipo=int,
            rango=(60, 275)
        )

        peso: int = self.obtener_entrada(
            mensaje="Ingrese su peso en kilogramos [2-635] >> ",
            tipo=int,
            rango=(2, 635)
        )

        fuma: bool = bool(
            self.obtener_entrada(
                mensaje="¿Fuma? [0 = No, 1 = Sí] >> ",
                tipo=int,
                opciones=[0, 1]
            )
        )

        alcohol: bool = bool(
            self.obtener_entrada(
                mensaje="¿Bebe alcohol? [0 = No, 1 = Sí] >> ",
                tipo=int,
                opciones=[0, 1]
            )
        )

        activo: bool = bool(
            self.obtener_entrada(
                mensaje="¿Es activo físicamente? [0 = No, 1 = Sí] >> ",
                tipo=int,
                opciones=[0, 1]
            )
        )

        return nombre, edad_dias, genero, altura, peso, fuma, alcohol, activo

    def obtener_entrada(self, mensaje: str, tipo: type, rango: tuple = None, opciones: list = None):
        """
        Obtiene y valida una entrada del usuario.
        Args:
            mensaje: El mensaje que se muestra al usuario.
            tipo: El tipo de dato esperado (e.g., int, str, bool).
            rango: Una tupla con el rango permitido (min, max).
            opciones: Una lista con valores permitidos.
        """
        while True:
            try:
                valor = tipo(input(mensaje))
                if rango and not (rango[0] <= valor <= rango[1]):
                    print(f"El valor debe estar entre {rango[0]} y {rango[1]}.")
                    continue
                if opciones and valor not in opciones:
                    print(f"El valor debe ser uno de los siguientes: {', '.join(map(str, opciones))}.")
                    continue
                return valor
            except ValueError:
                print("Entrada inválida. Por favor, intenta nuevamente.")

    def revisar_sesion(self):
        """
        Metodo que verifica si hay usuarios existentes en la base de datos.
        """
        if self.TABLA_USUARIOS.obtener_registro(id_usuario=self.ID_USER) == {}:

            # ▬▬▬▬ Asignamos usuario desconocido ▬▬▬▬ #
            self.FILE.actualizar_json(file_path=self.PATH_SAVE_FILE,clave="id_session",nuevo_valor=-1)
            self.ID_USER = self.FILE.cargar_json(file_path=self.PATH_SAVE_FILE)["id_session"]

            if self.TABLA_USUARIOS.obtener() == []:
                # ▬▬▬▬ Creamos un nuevo usuario ▬▬▬▬ #
                self.ejecutarComando(comando=7)
            else:
                # ▬▬▬▬ Seleccionamos otro usuario ▬▬▬▬ #
                self.ejecutarComando(comando=6)

    # ➤➤➤➤➤➤➤➤➤➤➤➤➤➤➤➤➤➤➤➤➤➤➤➤➤➤➤➤➤➤➤➤➤➤➤ CONTROLADOR ➤➤➤➤➤➤➤➤➤➤➤➤➤➤➤➤➤➤➤➤➤➤➤➤➤➤➤➤➤➤➤➤➤➤➤ #

    def iniciar(self):
        self.VIEW.showIntro()
        self.revisar_sesion()
        self.listar_comandos()

    def listar_comandos(self):
        comando: int = 0

        # ▬▬▬▬ Mostrara prompts hasta que el usuario desee salir de la aplicacion ▬▬▬▬ #
        while (comando != 10):
            self.revisar_sesion()
            self.VIEW.mostrarComandos(nombre=self.obtener_nombre())

            comando: int = self.obtener_entrada(
                mensaje="¿Que deseas hacer? [1-10] >>> ",
                rango=(1, 10),
                tipo=int
            )

            self.ejecutarComando(comando=comando)

    def ejecutarComando(self, comando):
        match comando:
            case 1:
                # ▬▬▬▬ 1) Registro completo de mi salud cardiovascular ▬▬▬▬ #
                self.obtener_registro_completo()

            case 2:
                # ▬▬▬▬ 2) Último registro cardiovascular. ▬▬▬▬ #
                self.obtener_ultimo_registro()
            case 3:
                # ▬▬▬▬ 3) Ver mis datos biométricos. ▬▬▬▬ #
                self.obtener_datos_biometricos()
            case 4:
                # ▬▬▬▬ 4) Modificar datos biométricos. ▬▬▬▬ #
                self.obtener_datos_biometricos()
                self.modificar_usuario()
                self.obtener_datos_biometricos()
            case 5:
                # ▬▬▬▬ 5) Ver usuarios registrados. ▬▬▬▬ #
                self.obtener_usuarios()
            case 6:
                # ▬▬▬▬ 6) Cambiar usuario. ▬▬▬▬ #
                self.obtener_usuarios()
                self.cambiar_usuario()
                self.obtener_datos_biometricos()
            case 7:
                # ▬▬▬▬ 7) Crear usuario. ▬▬▬▬ #
                self.crear_usuario()
            case 8:
                # ▬▬▬▬ 8) Borrar usuario. ▬▬▬▬ #
                self.obtener_usuarios()
                self.borrar_usuario()
                self.obtener_usuarios()
            case 9:
                # ▬▬▬▬ 9) Consultar modelo de predicción. ▬▬▬▬ #
                self.consultar_modelo()
            case 10:
                # ▬▬▬▬ 10) Salir ▬▬▬▬ #
                self.VIEW.mostrarDespedida()
            case _:
                # ▬▬▬▬ Si no se ejecuta un comando establecido ▬▬▬▬ #
                return

    def obtener_registro_completo(self):

        # ▬▬▬▬ Obtenemos la lista de tuplas de la base de datos. ▬▬▬▬ #
        registros: list = self.TABLA_REGISTROS.obtener(id_usuario=self.ID_USER)

        # ▬▬▬▬ Cabecera ▬▬▬▬ #
        resultado = f"""
╓───────────────────╥──────────────╥────────────────────╥─────────────────────╥──────────────╥──────────╖
║ {'Fecha':<17} ║ {'ID Usuario':<12} ║ {'Presión Sistólica':<18} ║ {'Presión Diastólica':<19} ║ {'Colesterol':<12} ║ {'Glucosa':<8} ║
╠───────────────────╬──────────────╬────────────────────╬─────────────────────╬──────────────╬──────────╣
        """

        # ▬▬▬▬ Agregar los registros ▬▬▬▬ #
        for registro in registros:
            fecha, id_usuario, ap_hi, ap_lo, cholesterol, gluc = registro

            # ▬▬▬▬ Convertir valores a enteros ▬▬▬▬ #
            cholesterol = self.convertir_a_enteros(valor_byte=cholesterol)
            gluc = self.convertir_a_enteros(valor_byte=gluc)

            # ▬▬▬▬ Convertir la fecha a formato de cadena ▬▬▬▬ #
            fecha_str = fecha.strftime('%Y-%m-%d %H:%M:%S')

            # ▬▬▬▬ Formatea registro ▬▬▬▬ #
            resultado += f"║ {fecha_str:<17} ║ {id_usuario:<12} ║ {ap_hi:<18} ║ {ap_lo:<19} ║ {cholesterol:<12} ║ {gluc:<8} ║\n"

        self.VIEW.mostrarRegistroCompleto(registro_completo=resultado)

    def obtener_ultimo_registro(self):

        # ▬▬▬▬ Obtenemos la ultima tupla de la base de datos. ▬▬▬▬ #
        fecha, id_usuario, ap_hi, ap_lo, cholesterol, gluc = self.TABLA_REGISTROS.obtener_ultimo(
            id_usuario=self.ID_USER)

        # ▬▬▬▬ Cabecera ▬▬▬▬ #
        resultado = f"""
        ╓───────────────────╥──────────────╥────────────────────╥─────────────────────╥──────────────╥──────────╖
        ║ {'Fecha':<17} ║ {'ID Usuario':<12} ║ {'Presión Sistólica':<18} ║ {'Presión Diastólica':<19} ║ {'Colesterol':<12} ║ {'Glucosa':<8} ║
        ╠───────────────────╬──────────────╬────────────────────╬─────────────────────╬──────────────╬──────────╣
"""

        # ▬▬▬▬ Convertir valores a enteros ▬▬▬▬ #
        cholesterol = self.convertir_a_enteros(valor_byte=cholesterol)
        gluc = self.convertir_a_enteros(valor_byte=gluc)

        # ▬▬▬▬ Convertir la fecha a formato de cadena ▬▬▬▬ #
        fecha_str = fecha.strftime('%Y-%m-%d %H:%M:%S')

        # ▬▬▬▬ Formatea registro ▬▬▬▬ #
        resultado += f"""
        ║ {fecha_str:<17} ║ {id_usuario:<12} ║ {ap_hi:<18} ║ {ap_lo:<19} ║ {cholesterol:<12} ║ {gluc:<8} ║\n
"""

        self.VIEW.mostrarUltimoRegistro(registro=resultado)

    def obtener_datos_biometricos(self):
        # ▬▬▬▬ Obtenemos la tupla de la informacion del usuario de la base de datos. ▬▬▬▬ #
        id, name, age, gender, height, weight, smoke, alco, active = self.TABLA_USUARIOS.obtener_registro(
            id_usuario=self.ID_USER)

        # ▬▬▬▬ Convertir dias a años ▬▬▬▬ #
        age = f"Dias({age})|Años({self.convertir_days_years(dias=age)})"

        # ▬▬▬▬ Formatear campos ▬▬▬▬ #
        gender = f"{"Masculino" if self.convertir_a_enteros(valor_byte=gender) == 2 else "Femenino"}"
        smoke = f"{"Si" if self.convertir_a_enteros(valor_byte=smoke) == 1 else "No"}"
        alco = f"{"Si" if self.convertir_a_enteros(valor_byte=alco) == 1 else "No"}"
        active = f"{"Si" if self.convertir_a_enteros(valor_byte=active) == 1 else "No"}"

        # ▬▬▬▬ Crear la tabla con los datos formateados ▬▬▬▬ #
        resultado = f"""
            ╓─────────────────────╥────────────────────────────────────────╖
            ║ {'Campo'}               ║ {'Resultado'}                              ║
            ╠─────────────────────╬────────────────────────────────────────╣
            ║ {'ID':<18}  ║{id:<30}          ║
            ║ {'Edad':<18}  ║{age:<30}          ║
            ║ {'Nombre':<18}  ║{name:<30}          ║
            ║ {'Género':<18}  ║{gender:<30}          ║
            ║ {'Altura':<18}  ║{height:<30}          ║
            ║ {'Peso':<18}  ║{weight:<30}          ║
            ║ {'¿Fuma?':<18}  ║{smoke:<30}          ║
            ║ {'¿Toma alcohol?':<18}  ║{alco:<30}          ║
            ║ {'Activo físicamente:':<18} ║{active:<30}          ║
            ╚═════════════════════╩════════════════════════════════════════╝
            """
        self.VIEW.mostrarDatosBiometricos(datos_biometricos=resultado)

    def modificar_usuario(self):
        self.VIEW.mostrarConfigurador(opcion="[4] Modificar datos biométricos.")

        # ▬▬▬▬ Validamos las entradas del usuario. ▬▬▬▬ #
        try:
            nombre, edad_dias, genero, altura, peso, fuma, alcohol, activo = self.mostrar_inputs_usuario()

            # ▬▬▬▬ Actualizamos el perfil del usuario. ▬▬▬▬ #
            self.TABLA_USUARIOS.actualizar(
                id=self.ID_USER,
                nombre=nombre,
                edad=edad_dias,
                genero=genero,
                altura=altura,
                peso=peso,
                fuma=fuma,
                alcohol=alcohol,
                fis_activo=activo
            )

        except Exception as e:
            print(f"Error: {e}. Por favor, intenta ingresar datos actualizables")

    def obtener_usuarios(self):
        # ▬▬▬▬ Obtenemos la lista de tuplas de la base de datos. ▬▬▬▬ #
        registros: list = self.TABLA_USUARIOS.obtener()

        # ▬▬▬▬ Cabecera ▬▬▬▬ #
        resultado = f"""
        ╓───────────────────╥──────────────╥────────────────────╥─────────────────────╥──────────────╥──────────╖──────────╖────────── ╖──────────     ╖
        ║ {'ID':<17} ║ {'Nombre':<12} ║ {'Edad':<18} ║ {'Genero':<19} ║ {'Altura':<12} ║ {'Peso':<8} ║ {'¿Fuma?':<8} ║ {'¿Alcohol?':<8} ║ {'¿Fis. Activo?':<8} ║
        ╠───────────────────╬──────────────╬────────────────────╬─────────────────────╬──────────────╬──────────╣──────────╣────────── ╣──────────     ╣
                """

        # ▬▬▬▬ Agregar los registros ▬▬▬▬ #
        for registro in registros:
            id, name, age, gender, height, weight, smoke, alco, active = registro

            # ▬▬▬▬ Convertir dias a años ▬▬▬▬ #
            age = f"Dias({age})|Años({self.convertir_days_years(dias=age)})"

            # ▬▬▬▬ Formatear campos ▬▬▬▬ #
            gender = f"{"Masculino" if self.convertir_a_enteros(valor_byte=gender) == 2 else "Femenino"}"
            smoke = f"{"Si" if self.convertir_a_enteros(valor_byte=smoke) == 1 else "No"}"
            alco = f"{"Si" if self.convertir_a_enteros(valor_byte=alco) == 1 else "No"}"
            active = f"{"Si" if self.convertir_a_enteros(valor_byte=active) == 1 else "No"}"

            # ▬▬▬▬ Formatea registro ▬▬▬▬ #
            resultado += f"\n║ {id:<17} ║ {name:<12} ║ {age:<18} ║ {gender:<19} ║ {height:<12} ║ {weight:<8} ║ {smoke:<8} ║ {alco:<8} ║ {active:<8} ║"

        self.VIEW.mostrarUsuariosRegistrados(usuarios_registrados=resultado)

    def cambiar_usuario(self):
        self.VIEW.mostrarConfigurador(opcion="[6] Cambiar usuario.")

        # ▬▬▬▬ Obtenemos la lista de tuplas de la base de datos. ▬▬▬▬ #
        registros: list = self.TABLA_USUARIOS.obtener()
        opciones = []

        # ▬▬▬▬ Guardamos todos los ID disponibles a escoger ▬▬▬▬ #
        for registro in registros:
            id, name, age, gender, height, weight, smoke, alco, active = registro
            opciones.append(id)

        # ▬▬▬▬ Validamos las entradas del usuario. ▬▬▬▬ #
        try:
            choice: int = self.obtener_entrada(
                mensaje="Seleccione un usuario registrado >> ",
                tipo=int,
                opciones=opciones
            )

            # ▬▬▬▬ Cambiamos de sesion de usuario. ▬▬▬▬ #
            self.FILE.actualizar_json(file_path=self.PATH_SAVE_FILE, clave="id_session", nuevo_valor=choice)
            self.ID_USER = self.FILE.cargar_json(file_path=self.PATH_SAVE_FILE)["id_session"]

        except Exception as e:
            print(f"Error: {e}. Por favor, intenta ingresar datos válidos.")

    def crear_usuario(self):
        self.VIEW.mostrarConfigurador(opcion="[7] Crear usuario.")

        # ▬▬▬▬ Validamos las entradas del usuario. ▬▬▬▬ #
        try:
            nombre, edad_dias, genero, altura, peso, fuma, alcohol, activo = self.mostrar_inputs_usuario()

            # ▬▬▬▬ Actualizamos el perfil del usuario. ▬▬▬▬ #
            self.TABLA_USUARIOS.crear(
                nombre=nombre,
                edad=edad_dias,
                genero=genero,
                altura=altura,
                peso=peso,
                fuma=fuma,
                alcohol=alcohol,
                fis_activo=activo
            )

            # ▬▬▬▬ Obtenemos la tupla de la informacion del ultimo usuario registrado de la base de datos. ▬▬▬▬ #
            id, name, age, gender, height, weight, smoke, alco, active = self.TABLA_USUARIOS.obtener_ultimo_registro()

            # ▬▬▬▬ Convertir dias a años ▬▬▬▬ #
            age = f"Dias({age})|Años({self.convertir_days_years(dias=age)})"

            # ▬▬▬▬ Formatear campos ▬▬▬▬ #
            gender = f"{"Masculino" if self.convertir_a_enteros(valor_byte=gender) == 2 else "Femenino"}"
            smoke = f"{"Si" if self.convertir_a_enteros(valor_byte=smoke) == 1 else "No"}"
            alco = f"{"Si" if self.convertir_a_enteros(valor_byte=alco) == 1 else "No"}"
            active = f"{"Si" if self.convertir_a_enteros(valor_byte=active) == 1 else "No"}"

            # ▬▬▬▬ Crear la tabla con los datos formateados ▬▬▬▬ #
            resultado = f"""
                        ╓─────────────────────╥────────────────────────────────────────╖
                        ║ {'Campo'}               ║ {'Resultado'}                              ║
                        ╠─────────────────────╬────────────────────────────────────────╣
                        ║ {'ID':<18}  ║{id:<30}          ║
                        ║ {'Edad':<18}  ║{age:<30}          ║
                        ║ {'Nombre':<18}  ║{name:<30}          ║
                        ║ {'Género':<18}  ║{gender:<30}          ║
                        ║ {'Altura':<18}  ║{height:<30}          ║
                        ║ {'Peso':<18}  ║{weight:<30}          ║
                        ║ {'¿Fuma?':<18}  ║{smoke:<30}          ║
                        ║ {'¿Toma alcohol?':<18}  ║{alco:<30}          ║
                        ║ {'Activo físicamente:':<18} ║{active:<30}          ║
                        ╚═════════════════════╩════════════════════════════════════════╝
                        """
            self.VIEW.mostrarDatosBiometricos(datos_biometricos=resultado)

            # ▬▬▬▬ Cambiamos de sesion al perfil creado ▬▬▬▬ #
            self.FILE.actualizar_json(file_path=self.PATH_SAVE_FILE, clave="id_session", nuevo_valor=id)
            self.ID_USER = self.FILE.cargar_json(file_path=self.PATH_SAVE_FILE)["id_session"]

        except Exception as e:
            print(f"Error: {e}. Por favor, intenta ingresar datos que pueda crear un usuario")

    def borrar_usuario(self):
        self.VIEW.mostrarConfigurador(opcion="[8] Borrar usuario.")

        # ▬▬▬▬ Obtenemos la lista de tuplas de la base de datos. ▬▬▬▬ #
        registros: list = self.TABLA_USUARIOS.obtener()
        opciones = []

        # ▬▬▬▬ Guardamos todos los ID disponibles a escoger ▬▬▬▬ #
        for registro in registros:
            id, name, age, gender, height, weight, smoke, alco, active = registro
            opciones.append(id)

        # ▬▬▬▬ Validamos las entradas del usuario. ▬▬▬▬ #
        try:
            choice: int = self.obtener_entrada(
                mensaje="Seleccione un usuario registrado que quiera eliminar >> ",
                tipo=int,
                opciones=opciones
            )

            # ▬▬▬▬ Eliminamos el usuario de la base de datos ▬▬▬▬ #
            self.TABLA_USUARIOS.eliminar(id=choice)

        except Exception as e:
            print(f"Error: {e}. Por favor, intenta ingresar datos válidos.")

    def consultar_modelo(self):
        self.VIEW.mostrarModelo(summario=self.PREDICTER.resumen_modelo())


if __name__ == '__main__':
    dataset = pd.read_csv(filepath_or_buffer="../model/cardio_train.csv", sep=';')
    predict = Predicter(dataset=dataset)
    predict.entrenar_modelo(max_iter=100, test_size=0.3, ramdom_state=0)
    tabla_registro = Register(user="adminCV", pwd="admin123")
    tabla_usuarios = User(user="adminCV", pwd="admin123")
    vista = Console()

    controlador = ViewModel(
        predictor=predict,
        usuarios=tabla_usuarios,
        registros=tabla_registro,
        vista=vista
    )

    controlador.iniciar()
