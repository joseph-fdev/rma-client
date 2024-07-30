import sqlite3
import requests
import asyncio
conexion = sqlite3.connect("rma.db")
try:
    conexion.execute(
        """create table articulos (
                              fecha integer primary key autoincrement,
                              hora_inicio text,
                              hora_fin text,
                              id_esp32 text

                        )"""
    )
    print("se creo la tabla articulos")

except sqlite3.OperationalError:
    print("La tabla articulos ya existe")
conexion.close()
