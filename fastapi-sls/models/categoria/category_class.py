from db import execute_query

class Categoria:
    def create_cat(self, id: int, name: str):
        query = "INSERT INTO categorias (Cat_id, Cat_name) VALUES (%s, %s)"
        try:
            execute_query(query, (id, name), commit=True)
            return {"Cat_id": id, "Cat_name": name}
        except Exception as e:
            print(f"Error al crear una categoria: {e}")
            return False
        
    def all_categories(self):
        query="SELECT * FROM categorias"
        try:
            categorias = execute_query(query,fetchall=True)  
            return categorias
        except Exception as e:
            print(f"Error al mostrar las categorias : {e}")
            return []
        
    def delete_cat(self, id: int):
        query = "DELETE FROM categorias WHERE Cat_id = %s"
        try:
            execute_query(query, (id,), commit=True)
            return True
        except Exception as e:
            print(f"Error al borrar una categoria: {e}")
            return False