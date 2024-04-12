def insertar_localidad(instancia=None, datos=None):
    if not instancia:
        return None
    if not datos:
        return None
    
    consulta_insertar_localidad = """
    INSERT INTO provincias (provincia, id, localidad, cp, id_prov_mstr)
    VALUES (%s, %s, %s, %s, %s)
    """
    
    cursor = instancia.cursor()
    cursor.executemany(consulta_insertar_localidad, datos)
    
    instancia.commit()
    
    cursor.close()