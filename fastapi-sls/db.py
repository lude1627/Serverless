import mysql.connector

conexion = mysql.connector.connect(
   user = "root",
   password = "",
    host = "localhost",
    database = "project",
    port = 3306,
    )



def execute_query(query: str, params = (), fetchone=False, fetchall=False, commit=False, return_id=False):
    cursor = conexion.cursor()

    
    cursor.execute(query, params or ())

    result = None
    if fetchone:
        result = cursor.fetchone()
    elif fetchall:
        result = cursor.fetchall()
    
    if commit:
        conexion.commit()
        return cursor.rowcount

    if return_id:   
        result = cursor.lastrowid
    
    cursor.close()
    return result


