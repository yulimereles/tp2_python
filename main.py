import os
import csv
import MySQLdb

# Función para leer el archivo CSV y devolver una lista de filas.
def read_csv(file_path):
    try:
        with open(file_path, newline='') as archivo_csv:
            lector_csv = csv.reader(archivo_csv, delimiter=',', quotechar='"')
            return list(lector_csv)
    except FileNotFoundError as e:
        print(f'No se encontró el archivo. Error: {e}')
        return []

# Función para conectarse a la base de datos MySQL.
def connect_db(host, user, password, database):
    try:
        db = MySQLdb.connect(host, user, password, database)
        print("Conexión a la base de datos exitosa.")
        return db
    except MySQLdb.Error as e:
        print("No se pudo conectar a la base de datos:", e)
        return None

# Función para crear la tabla en la base de datos e insertar datos desde el CSV.
def create_table_and_insert_data(db, table_name, csv_data):
    if db is None:
        print("Error: No se ha establecido conexión a la base de datos.")
        return

    try:
        cursor = db.cursor()
        cursor.execute(f"DROP TABLE IF EXISTS {table_name}")
        cursor.execute(f"CREATE TABLE IF NOT EXISTS {table_name} ( provincia VARCHAR(200), id INT, localidad VARCHAR(255), cp VARCHAR(255), id_prov_mstr VARCHAR(200))")
        
        for row in csv_data:
            cursor.execute(f"INSERT INTO {table_name} (provincia, id, localidad, cp, id_prov_mstr) VALUES (%s, %s, %s, %s, %s)", row)
        
        db.commit()
        print("Tabla creada e datos insertados correctamente.")
    except MySQLdb.Error as e:
        print("Error al crear la tabla o insertar datos:", e)

# Función para agrupar y exportar datos por provincia.
def group_and_export_data(db, table_name, output_folder):
    if db is None:
        print("Error: No se ha establecido conexión a la base de datos.")
        return

    try:
        cursor = db.cursor()
        cursor.execute(f"SELECT DISTINCT provincia FROM {table_name}")
        provincias = cursor.fetchall()
        
        for provincia in provincias:
            cursor.execute(f"SELECT * FROM {table_name} WHERE provincia = %s", (provincia[0],))
            rows = cursor.fetchall()
            
            with open(os.path.join(output_folder, f'{provincia[0]}.csv'), 'w', newline='') as file:
                writer = csv.writer(file)
                writer.writerows(rows)
        
        print('Agrupación y exportación exitosa.')
    except MySQLdb.Error as e:
        print('Error al agrupar y exportar. Error:', e)

# Ejemplo de uso de las funciones:
if __name__ == "__main__":
    # Leer el archivo CSV
    csv_file = 'localidades.csv'
    csv_data = read_csv(csv_file)

    # Conectar a la base de datos
    db = connect_db("localhost", "root", "", "provincias")

    # Crear la tabla y insertar datos desde el CSV
    if db is not None:
        create_table_and_insert_data(db, "localidades", csv_data)

    # Agrupar y exportar datos por provincia
    output_folder = 'Provincias_csv'
    group_and_export_data(db, "localidades", output_folder)

    # Cerrar la conexión a la base de datos
    if db is not None:
        db.close()
