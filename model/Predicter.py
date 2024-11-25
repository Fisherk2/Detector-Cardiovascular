"""
============================================================
17/11/24
INTELIGENCIA ARTIFICIAL
Predictor de fulminación por paro cardiaco.

Equipo 8
Silva Pedraza Christian Ernesto
Villafaña Oliva César Omar
Zúñiga Gómez Jóse Alberto
============================================================
"""

import pandas as pd
from pandas import DataFrame
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report, confusion_matrix, accuracy_score
from sklearn.preprocessing import StandardScaler


class Predicter:
    """
    Clase que almacena y entrena los registros obtenidos de la base de datos para un model de
    regresion logistica multiple con el fin de predecir si el usuario esta a punto de tener un paro cardiaco o no.
    """

    def __init__(self, dataset: DataFrame):
        """
        Clase que almacena y entrena los registros obtenidos de la base de datos, con el fin de entrenar un model de
        regresion logistica multiple con el fin de predecir si el usuario esta a punto de tener un paro cardiaco o no.
        Args:
            dataset:
                Registro cardiovascular con estos campos:
                    Age | Objective Feature | age | int (days)
                    Height | Objective Feature | height | int (cm) |
                    Weight | Objective Feature | weight | float (kg) |
                    Gender | Objective Feature | gender | categorical code (1 - women, 2 - men) |
                    Systolic blood pressure | Examination Feature | ap_hi | int |
                    Diastolic blood pressure | Examination Feature | ap_lo | int |
                    Cholesterol | Examination Feature | cholesterol | 1: normal, 2: above normal, 3: well above normal |
                    Glucose | Examination Feature | gluc | 1: normal, 2: above normal, 3: well above normal |
                    Smoking | Subjective Feature | smoke | binary |
                    Alcohol intake | Subjective Feature | alco | binary |
                    Physical activity | Subjective Feature | active | binary |
                    Presence or absence of cardiovascular disease | Target Variable | cardio | binary |
        """

        # ▬▬▬▬ Renombramos la variable dependiente como el objetivo de nuestro model ▬▬▬▬ #
        self.df = dataset.rename(columns={'cardio': 'target'})
        self.scaler = StandardScaler()
        self.modelo = None

    def entrenar_modelo(self, test_size: float = 0.2, ramdom_state: int = 42, max_iter: int = 5000):
        """
        Metodo que ajusta el model de regresion logistica multiple.
        Args:
            test_size: Tamaño de la prueba de entrenamiento(0.20 = 20%)
            ramdom_state: Estado de prediccion que puede ser cualquier numero entero.
            max_iter: Número máximo de iteraciones que el algoritmo de optimización utilizará para converger hacia una solución

        """
        # ▬▬▬▬ Determinamos las variables dependientes e independientes ▬▬▬▬ #
        self.X = self.df.drop(columns='target', axis=1)  # Independientes
        y = self.df['target']  # Dependientes

        # ▬▬▬▬ Dividir los datos en conjunto de entrenamiento y prueba ▬▬▬▬ #
        X_train, X_test, y_train, self.y_test = train_test_split(self.X, y, test_size=test_size,
                                                                 random_state=ramdom_state)

        # ▬▬▬▬ Estandarizamos los datos de tal manera que tengan una media de 0 y una desviación estándar de 1. ▬▬▬▬ #
        self.X_train_scaled = self.scaler.fit_transform(X_train)
        self.X_test_scaled = self.scaler.transform(X_test)

        # ▬▬▬▬ Ajustar el model de regresión logística ▬▬▬▬ #
        self.modelo = LogisticRegression(max_iter=max_iter)
        self.modelo.fit(self.X_train_scaled, y_train)

    def resumen_modelo(self) -> str:
        # ▬▬▬▬ En caso de que el modelo aún no haya sido entrenado ▬▬▬▬ #
        if self.modelo is None:
            raise ValueError("El modelo no está entrenado.")

        # ▬▬▬▬ Generamos predicciones de las pruebas. ▬▬▬▬ #
        y_pred = self.modelo.predict(self.X_test_scaled)

        # ▬▬▬▬ Construimos el reporte ▬▬▬▬ #
        report = []

        report.append("""
        ┌─────────────────────────────────────────────────────────────────────┐
        │                       ✧✧ MATRIZ DE CONFUSIÓN ✧✧                    │
        └─────────────────────────────────────────────────────────────────────┘
        """)
        conf_matrix = confusion_matrix(self.y_test, y_pred)
        verdaderos_negativos, falsos_positivos, falsos_negativos, verdaderos_positivos = (
            conf_matrix[0, 0], conf_matrix[0, 1], conf_matrix[1, 0], conf_matrix[1, 1]
        )
        report.append(str(conf_matrix))
        report.append(
            f"✔ Correctos (No paro cardiaco): {verdaderos_negativos} persona{'s' if verdaderos_negativos != 1 else ''}."
        )
        report.append(
            f"✔ Correctos (Paro cardiaco): {verdaderos_positivos} persona{'s' if verdaderos_positivos != 1 else ''}."
        )
        report.append(
            f"✘ Falsos negativos: {falsos_negativos} persona{'s' if falsos_negativos != 1 else ''}."
        )
        report.append(
            f"✘ Falsos positivos: {falsos_positivos} persona{'s' if falsos_positivos != 1 else ''}."
        )

        report.append("""
        ┌─────────────────────────────────────────────────────────────────────┐
        │                   ✧✧ REPORTE DE CLASIFICACIÓN ✧✧                   │
        └─────────────────────────────────────────────────────────────────────┘
        """)
        class_report = classification_report(self.y_test, y_pred)
        report.append(class_report)

        report.append("""
        ┌─────────────────────────────────────────────────────────────────────┐
        │                        ✧✧ INTERCEPTO ✧✧                            │
        └─────────────────────────────────────────────────────────────────────┘
        """)
        intercepto = self.modelo.intercept_[0]
        report.append(f"Intercepto: {intercepto}")

        report.append("""
        ┌─────────────────────────────────────────────────────────────────────┐
        │                   ✧✧ TABLA DE COEFICIENTES ✧✧                      │
        └─────────────────────────────────────────────────────────────────────┘
        """)
        df_coeficientes = DataFrame({
            "Feature": self.X.columns,
            "Coefficient": self.modelo.coef_[0]
        })
        report.append(df_coeficientes.to_string(index=False))

        return "\n".join(report)

    def predecir_multiple(self, dataset: DataFrame) -> DataFrame:
        """
        Funcion que generara multiples predicciones de un registro para determinar la probabilidad de que le fuera dar
        un paro cardiaco.
        Args:
            dataset: Registros multiples donde se almacena los datos del usuario.

        Returns:
            Dataframe, con una nueva columna donde verifica la probabilidad de haber tenido un paro cardiaco en
            cada registro.
        """

        # ▬▬▬▬ En caso de que el model aun no haya sido entrenado ▬▬▬▬ #
        if self.modelo is None:
            raise ValueError("El model no está entrenado.")

        # ▬▬▬▬ Escalamos los registros ▬▬▬▬ #
        df_escalado = self.scaler.transform(dataset)

        # ▬▬▬▬ Generamos predicciones de cada registro ▬▬▬▬ #
        probabilidades = self.modelo.predict_proba(df_escalado)
        dataset['Probabilidad_Paro_Cardiaco'] = probabilidades[:, 1]  # Probabilidades de clase 1

        return dataset

    def predecir_registro(self, registro: DataFrame) -> tuple[int, float, float]:
        """
        Funcion que generara la prediccion de un registro para determinar si le va dar un paro cardiaco y las
        probabilidades de que suceda o no.
        Args:
            registro: DataFrame donde se almacena todos los datos del usuario.

        Returns:
            Tupla, donde el primer valor es si le va dar o no un paro cardiaco (0 ó 1),
            el segundo valor es el coeficiente de probabilidad de que NO le de un paro cardiaco (0.73 = 73%),
            el tercer valor es el coeficiente de probabilidad de que SI le de un paro cardiaco (0.27 = 27%).
        """
        # ▬▬▬▬ Escalamos el registro ▬▬▬▬ #
        registro_escalado = self.scaler.transform(registro)

        # ▬▬▬▬ Generamos prediccion (0 ó 1) y la probabilidad de no morir y si morir ▬▬▬▬ #
        prediccion = self.modelo.predict(registro_escalado)[0]
        probabilidad = self.modelo.predict_proba(registro_escalado)

        return prediccion, probabilidad[0][0], probabilidad[0][1]


if __name__ == '__main__':
    dataset = pd.read_csv(filepath_or_buffer='cardio_train.csv', sep=';')

    predictor = Predicter(dataset=dataset)
    predictor.entrenar_modelo(max_iter=100, test_size=0.3, ramdom_state=0)

    print(predictor.resumen_modelo())

    dataset_ejemplo = dataset.rename(columns={'cardio': 'target'})
    dataset_ejemplo = dataset_ejemplo.drop(columns='target', axis=1)
    print(predictor.predecir_multiple(dataset=dataset_ejemplo).head(n=10))

    df_registro = DataFrame(data={
        "id": [33],
        "age": [9_862], #Dias (27 años)
        "gender": [2],
        "height": [176], #cm
        "weight": [80], #kg
        "ap_hi": [110],
        "ap_lo": [70],
        "cholesterol": [1],
        "gluc": [1],
        "smoke": [0],
        "alco": [0],
        "active": [0]
    })

    prediccion, probabilidad_no_morir, probabilidad_morir = predictor.predecir_registro(df_registro)

    print(
        f'Prediccion: {prediccion}, por lo tanto {"te va dar" if prediccion == 1 else "no te va dar"} un paro cardiaco')
    print(
        f"Probabilidades: de que NO te vaya dar un paro cardiaco = {probabilidad_no_morir * 100} %, de que SI te vaya dar un paro cardiaco = {probabilidad_morir * 100} %")

