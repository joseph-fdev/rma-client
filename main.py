import sqlite3
import requests
import asyncio
import json
import datetime
import time


# se encarga de crerar la db en sqlite rma
def crear_db():
    conexion = sqlite3.connect("rma.db")
    try:
        conexion.execute(
            """create table backup (
                            id_esp32 text,
                              fecha text,
                              hora_inicio text,
                              hora_fin text
                        )"""
        )
        print("se creo la tabla backup")

    except sqlite3.OperationalError:
        print("La tabla articulos ya existe")
    conexion.close()


crear_db()

# def accionador():
#     try:
#         response = requests.get(api_url)
#         response.raise_for_status()  # Verificar si hubo un error en la petición

#         # Procesar el JSON
#         data = response.json()

#         # Verificar la condición en el JSON
#         if data.get("userId") == 2:
#             print("activado")
#         else:
#             print("No se activó el pin GPIO")

#     except requests.RequestException as e:
#         print(f"Error en la petición: {e}")
#     except Exception as e:
#         print(f"Error: {e}")


def consultar_api(api_url):

    response = requests.get(api_url)
    if response.status_code == 200:
        data = response.json()
        print(data)
        return data

    else:
        print(f"Error {response.status_code}: {response.text}")


def normalizar_datos(data):
    datos_procesados = []
    for i in data:
        p_datos = {
            "id_esp32": i.get("idEsp32"),
            "fecha": i.get("fecha"),
            "hora_inicio": i.get("hora_inicio"),
            "hora_fin": i.get("hora_fin"),
        }
        datos_procesados.append(p_datos)
    print("datos proce: ", datos_procesados)
    return datos_procesados


def insertar_datos(data):

    conexion = sqlite3.connect("rma.db")
    try:
        with conexion:
            print("se incio conect a db para ingresar datos")
            for item in data:
                conexion.execute(
                    "insert into backup (id_esp32, fecha, hora_inicio, hora_fin) Values (?, ?, ?, ?)",
                    (
                        item["id_esp32"],
                        item["fecha"],
                        item["hora_inicio"],
                        item["hora_fin"],
                    ),
                )
    except sqlite3.Error as e:
        print(f"No se pudo ingresar los datos: {e}")
    finally:
        conexion.close()


# Función principal que inicia el procesamiento de los datos
def iniciar_proceso(api_url):
    datos_crudos = consultar_api(api_url)
    datos_normalizados = normalizar_datos(datos_crudos)
    insertar_datos(datos_normalizados)
    print("Se completo el proceso")


hoy = datetime.date.today()
semana_actual = hoy.isocalendar().week

# conexion a la API
api_url = f"https://3p7jzhtc-8000.brs.devtunnels.ms/api/programaWeek/{semana_actual}/"

iniciar_proceso(api_url)


# Funciones post
def enviar_datos():
    print("funcion")


def validador():
    print("consulta la api primero")


datos = {"datos": "datos"}
