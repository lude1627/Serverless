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
                "data": {
                            "Cat_id": id, 
                            "Cat_name": name
                         }
            }, status_code=200)
            
        except Exception as e:
            
            if e.errno == 1062:
                return JSONResponse(content={
                    "success": False,
                    "message": f"El ID {id} ya existe, por favor use otro."
            }, status_code=400)

        except Exception as e:
            print(f"Error al crear una categoria: {e}")
        return JSONResponse(content={
            "success": False,
            "message": "Ocurrió un error inesperado al crear la categoría."
        }, status_code=500)
        
    def all_categories(self):
        query = "SELECT Cat_id, Cat_name FROM categorias"
        try:
            categorias = execute_query(query, fetchall=True)

            if categorias:
              
                 

                response = {
                    "success": True,
                    "message": "Categorías obtenidas exitosamente",
                    "data" : [{ "Cat_id": cat[0],"Cat_name": cat[1] }for cat in categorias]
                }
                return JSONResponse(content=response, status_code=200)

            else:
                response = {
                    "success": True,
                    "message": "No hay categorías registradas",
                    "data": []
                }
                return JSONResponse(content=response, status_code=200)

        except Exception as e:
            print(f"Error al obtener las categorias: {e}")
            response = {
                "success": False,
                "message": f"Error al obtener categorías: {e}",
                "data": []
            }
            return JSONResponse(content=response, status_code=500)


        
    def delete_cat(self, id: int):
        query = "DELETE FROM categorias WHERE Cat_id = %s"
        try:
            execute_query(query, (id,), commit=True)

            return JSONResponse(content={
                "success": True,
                "message": "Categoría eliminada exitosamente "
            }, status_code=200)

        except Exception as e:
            print(f"Error al borrar una categoria: {e}")
            return JSONResponse(content={
                "success": False,
                "message":"Error al eliminar categoría: "
            }, status_code=500)

