import csv
from pathlib import Path

def obtener_localidades(ruta):
    localidades = []
    with open(ruta, "r", encoding="utf-8") as archivo:
        lector = csv.reader(archivo)
        for fila in lector:
            localidades.append(fila)
    return localidades
