import MySQLdb


def db_connection ():
    db = MySQLdb.connect("localhost", "root", "", "provincias")
    return db