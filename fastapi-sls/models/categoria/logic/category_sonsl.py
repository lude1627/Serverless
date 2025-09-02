from db import execute_query

def create_cat(id: int, name: str):
    query = "INSERT INTO categorias (Cat_id, Cat_name) VALUES (%s, %s)"
    try:
        execute_query(query, (id, name), commit=True)
        return {"Cat_id": id, "Cat_name": name}
    except Exception as e:
        print("Error al crear una categoria: {e}")
        return False
    
def all_categories():
   
    query="SELECT * FROM categorias"
    try:
        categorias = execute_query(query,fetchall=True)  
        return categorias
    except Exception as e:

        print("Error al mostrar las categorias : {e}")
def delete_cat(id: int):
    query = "DELETE FROM categorias WHERE Cat_id = %s"
    try:
        execute_query(query, (id), commit=True)
        return True
    except Exception as e:
        print("Error al borrar una categoria: {e}")
        return False