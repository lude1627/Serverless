from db import execute_query
from fastapi.responses import JSONResponse

class Categoria:
    
    def create_cat(self, id: int, name: str):
        query = "INSERT INTO categorias (Cat_id, Cat_name) VALUES (%s, %s)"
        try:
            execute_query(query, (id, name), commit=True)
            
            return JSONResponse(content={
                "success": True,
                "message": "Categoría creada exitosamente",
                "data": {"Cat_id": id, 
                         "Cat_name": name
                         }
            }, status_code=200)
            
        except Exception as e:
            
            if e.errno == 1062:
                return JSONResponse(content={
                    "success": False,
                    "message": f"El ID {id} ya existe, por favor use otro."
            }, status_code=400)
            else:
                return JSONResponse(content={
                    "success": False,
                    "message": f"Error de integridad: {str(e)}"
            }, status_code=400)

        except Exception as e:
            print(f"Error al crear una categoria: {e}")
        return JSONResponse(content={
            "success": False,
            "message": "Ocurrió un error inesperado al crear la categoría."
        }, status_code=500)
        
        
    def all_categories(self):
        query="SELECT * FROM categorias"
        try:
            categorias = execute_query(query,fetchall=True)  
            if categorias:
                return JSONResponse(content={
                    "success": True,
                    "message": "Categorías obtenidas exitosamente",
                    "data": categorias
                }, status_code=200)
                
            else:
                return JSONResponse(content={
                    "success": True,
                    "message": "No hay categorías registradas",
                    "data": []
                }, status_code=200)
        except Exception as e:
            print(f"Error al obtener las categorias: {e}")
            return JSONResponse(content={
                "success": False,
                "message": f"Error al obtener categorías: {e}",
                "data": []
            }, status_code=500)
        
        
    def delete_cat(self, id: int):
        query = "DELETE FROM categorias WHERE Cat_id = %s"
        try:
            execute_query(query, (id,), commit=True)

            if execute_query("SELECT * FROM categorias WHERE Cat_id = %s", (id,), fetchone=True):
                return JSONResponse(content={
                    "success": False,
                    "message": "Categoría no encontrada"
                }, status_code=404)

            return JSONResponse(content={
                "success": True,
                "message": "Categoría eliminada exitosamente"
            }, status_code=200)

        except Exception as e:
            print(f"Error al borrar una categoria: {e}")
            return JSONResponse(content={
                "success": False,
                "message": "Error al eliminar categoría"
            }, status_code=500)

