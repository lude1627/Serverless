from db import execute_query
from fastapi.responses import JSONResponse
from models.user.user_entity import RegisterModel, UpdateUserModel

class validaU:
    def user_exist(id: int):
        check_query = "SELECT User_id FROM usuarios WHERE User_id = %s"
        try:
            existing_user = execute_query(check_query, (id,), fetchone=True)
            if existing_user:
                return JSONResponse(content={
                    "success": False,
                    "message": "El ID ya está registrado"
                }, status_code=409)  
        except Exception as e:
            print(f"Error al verificar usuario existente: {e}")
            return JSONResponse(content={
                "success": False,
                "message": "Error interno al verificar usuario existente"
            }, status_code=500)
