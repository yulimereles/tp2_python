def crear_tabla (instancia=None):
    if not instancia:
        return None
    
    eliminar_tabla = """
    DROP TABLE IF EXISTS provincias
    """
    
    consulta_crear_tabla = """
    CREATE TABLE IF NOT EXISTS provincias (
        id_provincia INT PRIMARY KEY AUTO_INCREMENT,
        provincia VARCHAR(255),
        id INTEGER,
        localidad VARCHAR(255),
        cp INTEGER,
        id_prov_mstr INTEGER
    )
    """
    
    # cursor:
    cursor = instancia.cursor()
    
    cursor.execute(eliminar_tabla)
    cursor.execute(consulta_crear_tabla)
    
    instancia.commit()
    
    cursor.close()