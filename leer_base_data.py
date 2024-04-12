def seleccionar_por_provincia(conn, provincia):
    consulta = """
    SELECT localidad, id, cp, id_prov_mstr FROM provincias WHERE provincia = %s
    """
    
    cursor = conn.cursor()
    cursor.execute(consulta, (provincia,))
    
    resultado = cursor.fetchall()
    
    cursor.close()
    
    return resultado


def obtener_provincias(conn):
    consulta = """
    SELECT DISTINCT provincia FROM provincias
    """
    
    provincias = []
    
    cursor = conn.cursor()
    cursor.execute(consulta)
    
    resultado = cursor.fetchall()
    
    for fila in resultado:
        provincias.append(fila[0])
    
    cursor.close()
    
    return provincias
