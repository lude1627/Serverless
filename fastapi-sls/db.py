import mysql.connector

conexion = mysql.connector.connect(
   user = "root",
   password = "",
    host = "localhost",
    database = "project",
    port = 3306,
    )



def execute_query(query: str, params: tuple = (), fetchone=False, fetchall=False, commit=False):
    cursor = conexion.cursor()
    cursor.execute(query, params)
    
    result = None
    if fetchone:
        result = cursor.fetchone()
    elif fetchall:
        result = cursor.fetchall()
    
    if commit:
        conexion.commit()
    
    cursor.close()
    return result