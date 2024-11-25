
# Detector cardiovascular

Este proyecto implementa un predictor de fulminación por paro cardiaco utilizando técnicas de inteligencia artificial, 
específicamente regresión logística. El sistema analiza datos y proporciona predicciones que pueden ser útiles para
prevenir paros cardiacos.

## Descripción

El proyecto está diseñado como una herramienta modular que incluye:
- **Modelos**: Para entrenar y predecir con datos cardiovasculares.
- **Base de datos**: Conexión y manejo de datos con MariaDB.
- **Interfaz en consola**: Para interactuar con el sistema de manera simple y efectiva.
- **Configuraciones**: Archivos y clases para administrar las configuraciones del sistema.

## Estructura del Proyecto

```
Detector-Cardiovascular/
├── App.py            # Archivo principal que ejecuta la aplicación.
├── Main.py           # Punto de entrada de la aplicación.
├── config/           # Configuraciones del sistema.
│   ├── Database.py   # Conexión y configuración de MariaDB.
│   ├── Fichero.py    # Manejo de archivos.
│   ├── Mail.py       # Configuración de correo electrónico.
│   ├── SMS.py        # Configuración para envío de SMS.
    ├── keys.json     # Configuración de credenciales de la aplicacion.
│   └── save.json     # Archivo de guardado de datos del usuario.
├── model/            # Modelos y datos.
│   ├── Predicter.py  # Implementación del predictor usando regresión logística.
│   ├── cardio_train.csv # Datos de entrenamiento.
│   ├── Paciente.py   # Clase para gestionar contactos de pacientes.
│   ├── User.py       # Registro para usuarios.
│   └── Register.py   # Registro de datos.
├── view/             # Vista del sistema.
│   └── Screen.py     # Interfaz basada en consola.
└── viewmodel/        # Lógica de negocio.
    ├── Prompt.py     # Gestión de entradas de usuario.
    └── Sensor.py     # Simulación de sensores.
```

## Requisitos Previos

- Python 3.8 o superior.
- Librerías necesarias:
```bash
   pip install pandas sckit-learn mariadb
   ```

## Instalación

1. Configura la base de datos en `config/Database.py`.

2. Configura el archivo de guardado `config/save.json`.
```bash
{
    "id_session": 1,                    # ID del usuario de la base de datos que iniciara sesion
    "pulse_timer": 30,                  # Tiempo de retraso por cada analisis del pulso del usuario
    "email": "user_email@example.com",  # Email donde se enviara alertas
    "phone_number": "5554443322",       # Numero telefonico que se enviara las alertas
    "chat_id_telegram": "1234567890"    # ID del chat del usuario que recibira alertas
}
   ```
3. Configura el archivo de credenciales `config/save.json`.
```bash
{
  "email_sender": "sender_email@example.com", #Email del que envia las alertas
  "pwd_app": "abcd efgh ijkl nmop",           #Contraseña de la app
  "smpt": "smtp.example.com",                 #Direccion del servicio de correos
  "bot_token_tg": "123456:ABC-DEF1234ghIkl-zyx57W2v1u123ew11",  #Token del bot de telegram
  "sms_sender": "+12223334455",               #Numero Telefonico que envia los SMS
  "sid": "1234567890ABCDEFGHIJKLMNOPQRSTUVWXYZ01",  #Cuenta SID de dicho numero telefonico
  "sid_auth": "abcdefghijklmnñopkrstuvwxyz12345"    #Token auth de la cuenta SID
}
   ```

## Uso

1. Ejecuta el archivo `Main.py` para iniciar la aplicación:
   ```bash
   python Main.py
   ```

2. Sigue las instrucciones en pantalla para consultar datos de los usuarios.

## Notas adicionales

Este proyecto puede mejorarse con una mejor arquitectura de base de datos y un mejor GUI para el usuario, el proyecto
esta modularizado para que se pueda implementar dichos requisitos.
