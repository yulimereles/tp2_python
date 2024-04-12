import csv
import pathlib
from conexion import db_connection
from crear_tabla import crear_tabla
from leer_localidades import obtener_localidades
from insertar_tablas import insertar_localidad
from leer_base_data import obtener_provincias, seleccionar_por_provincia

archivo_csv = "localidades.csv"

def formatear_nombre_archivo_csv(provincia):
    provincia = provincia.lower().replace(" ", "-")
    return f"{provincia}.csv"

def escribir_archivo_csv(archivo_csv, provincias):
    pathlib.Path(__file__).parent.joinpath("provincias", "localidades").mkdir(parents=True, exist_ok=True)
    path = pathlib.Path(__file__).parent.joinpath("provincias", "localidades", archivo_csv)
    with open(path, "w", newline="", encoding="utf-8") as archivo:
        escritor = csv.writer(archivo)
        escritor.writerows(provincias)
    return path

def main():
    # Se crea la conexión a la base de datos
    conn = db_connection()
    
    # Se crea la tabla para almacenar los datos
    crear_tabla(conn)
    
    # Se obtiene la ruta del archivo CSV
    ruta = pathlib.Path(__file__).parent.joinpath("provincias", archivo_csv)
    
    # Se obtienen las localidades del archivo CSV
    filas = obtener_localidades(ruta)
    
    # Se verifica si la primera fila es el encabezado y se omite
    if filas and filas[0][0].lower() == 'id':
        filas = filas[1:]
    
    # Se preparan los datos para insertar en la base de datos
    valores = []
    for fila in filas:
        # Se define una función auxiliar para verificar si el valor es numérico
        def convertir_a_entero(valor):
            try:
                return int(valor)
            except ValueError:
                return 0
        
        # Se prepara la fila para la inserción, utilizando la función auxiliar
        una_fila = (str(fila[0]), convertir_a_entero(fila[1]), str(fila[2]), convertir_a_entero(fila[3]), convertir_a_entero(fila[4]))
        valores.append(una_fila)
    
    # Se insertan los datos en la base de datos
    insertar_localidad(conn, valores)
    
    # Se obtiene una lista de las provincias
    provincias = obtener_provincias(conn)
    
    # Se obtienen todas las localidades por provincias
    for provincia in provincias:
        nombre_archivo = formatear_nombre_archivo_csv(provincia)
        resultado = seleccionar_por_provincia(conn, provincia)
        
        # Se crea y escribe el archivo CSV
        escribir_archivo_csv(nombre_archivo, resultado)
    
    # Se cierra la conexión a la base de datos
    conn.close()
    
if __name__ == "__main__":
    main()
