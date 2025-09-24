from db import execute_query
from fastapi.responses import JSONResponse

class Categoria:
    
    def create_cat(self, name: str):
        query = "INSERT INTO categorias (cat_name, cat_status) VALUES (%s, '1')"
        try:
        
            execute_query(query, (name,), commit=True)
            
            return JSONResponse(content={
                "success": True,
                "message": "Categoría creada exitosamente",
                "data": {
                            
                            "cat_name": name
                         }
            }, status_code=200)
           
        except Exception as e:
        
         return JSONResponse(content={
            "success": False,
            "message": f"Error al crear una categoria: {e}"
            }, status_code=500)
        
    def all_categories(self):
        query = "SELECT * FROM categorias"
        try:
            categorias = execute_query(query, fetchall=True)

            if categorias:
              
                 

                response = {
                    "success": True,
                    "message": "Categorías obtenidas exitosamente",
                    "data" : [{ 
                        "cat_id": cat[0],
                        "cat_name": cat[1], 
                        "cat_status": cat[2] 
                        }for cat in categorias]
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

            
            
    def update_cat(self, id: int, name: str, status: str):
        query = """
            UPDATE categorias 
            SET cat_name = %s, cat_status = %s
            WHERE cat_id = %s
        """
        try:
            execute_query(query, (name, status, id), commit=True)

            return JSONResponse(content={
                "success": True,
                "message": "Categoría actualizada exitosamente"
            }, status_code=200)

        except Exception as e:
            print(f"Error al actualizar la categoría: {e}")
            return JSONResponse(content={
                "success": False,
                "message": "Error al actualizar la categoría"
            }, status_code=500)


        
    def delete_cat(self, id: int):
        query = """
        UPDATE categorias 
        SET cat_status = '0' 
        WHERE cat_id = %s
        """
        
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

