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

class Console():
    """
    Clase que muestra graficamente el programa desde consola.
    """

    def showIntro(self):
        print("""
        ████████████████████████████████████████████████████████████████████████████
        █                                                                           █
        █                        DETECTOR CARDIOVASCULAR                            █
        █                         CONTRA PARO CARDIACO                              █
        █                                                                           █
        ████████████████████████████████████████████████████████████████████████████
        ███  ███   ██████    ██████   ██████   ██████   ██████   ████████  ███  ███
         ███ ███   ███  ███  ███      ███  ███ ███  ███ ███  ███    ███     ██████
          █████    ███  ███  ██████   ██████   ██████   ███  ███    ███      ████ 
         ███ ███   ███  ███      ███  ███      ███      ███  ███    ███     ██████
        ███   ███  ██████    ██████   ███      ███      ██████      ███    ███  ███
        ████████████████████████████████████████████████████████████████████████████
        █                                                                           █
        █                       Inteligencia Artificial                             █
        █                                                                           █
        ████████████████████████████████████████████████████████████████████████████

        Creado por: 
        Silva Pedraza Christian Ernesto
        Villafaña Oliva César Omar
        Zúñiga Gómez Jóse Alberto
            """)

    def mostrarComandos(self,nombre:str):
        print(f"""
        ══════════════════════════════════════════════════════════════════════════════════════════════
        Bienvenido {nombre}
        A continuación, ingresa la opción numérica de lo que quieras consultar sobre tu salud:
        
        ╭─────────────── REGISTRO PERSONAL ──────────────╮
        │ 1) Registro completo de mi salud cardiovascular│
        │    (Más reciente a más antiguo).               │
        │ 2) Último registro cardiovascular.             │
        ╰────────────────────────────────────────────────╯
        
        ╭──────────────── PERFIL USUARIO ───────────────╮
        │ 3) Ver mis datos biométricos.                 │
        │ 4) Modificar datos biométricos.               │
        ╰───────────────────────────────────────────────╯
        
        ╭──────────────── NUEVO USUARIO ────────────────╮
        │ 5) Ver usuarios registrados.                  │
        │ 6) Cambiar usuario.                           │
        │ 7) Crear usuario.                             │
        │ 8) Borrar usuario.                            │
        ╰───────────────────────────────────────────────╯
        
        ╭──────────────────── OTROS ────────────────────╮
        │ 9) Consultar modelo de predicción.            │
        ╰───────────────────────────────────────────────╯
        
        ╭───────────────────────╮
        │ 10) Salir             │
        ╰───────────────────────╯
        ══════════════════════════════════════════════════════════════════════════════════════════════
        """)

    def mostrarRegistroCompleto(self, registro_completo: str):
        print("""
        ╔══════════════════════════════════════════════════════════════════════════════════════════╗
        ║                  REGISTRO COMPLETO SOBRE TUS NIVELES CARDIOVASCULARES                    ║
        ╚══════════════════════════════════════════════════════════════════════════════════════════╝
        """)

        print(registro_completo)

    def mostrarUltimoRegistro(self, registro: str):
        print("""
        ╔══════════════════════════════════════════════════════════════════════════════════════════╗
        ║                     ULTIMO REGISTRO SOBRE TUS NIVELES CARDIOVASCULARES                   ║
        ╚══════════════════════════════════════════════════════════════════════════════════════════╝
        """)
        print(registro)

    def mostrarDatosBiometricos(self, datos_biometricos: str):
        print("""
        ╔══════════════════════════════════════════════════════════════════════════════════════════╗
        ║                                 DATOS BIOMETRICOS                                        ║
        ╚══════════════════════════════════════════════════════════════════════════════════════════╝
        """)
        print(datos_biometricos)

    def mostrarUsuariosRegistrados(self, usuarios_registrados: str):
        print("""
        ╔══════════════════════════════════════════════════════════════════════════════════════════╗
        ║                                USUARIOS REGISTRADOS                                      ║
        ╚══════════════════════════════════════════════════════════════════════════════════════════╝
        """)
        print(usuarios_registrados)

    def mostrarModelo(self, summario:str):
        print("""
        ╔══════════════════════════════════════════════════════════════════════════════════════════╗
        ║                            SUMARIO DE MODELO PREDICTIVO                                  ║
        ╚══════════════════════════════════════════════════════════════════════════════════════════╝
        """)
        print(summario)

    def mostrarConfigurador(self, opcion: str):
        print(f"""
        ┌──────────────────────────────────────────────────────────────────────────────────────────┐
                                            >> Configurar <<   
            >> {opcion}                                
        └──────────────────────────────────────────────────────────────────────────────────────────┘
        """)

    def mostrarDespedida(self):
        print("""
        ╔══════════════════════════════════════════════════════════════════════════════════════════╗
        ║                                     HASTA PRONTO                                         ║
        ╚══════════════════════════════════════════════════════════════════════════════════════════╝
        """)


if __name__ == '__main__':
    ...
