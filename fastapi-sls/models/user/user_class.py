from db import execute_query
from fastapi.responses import JSONResponse
from services.user_service.servicesU import validaU
import re

val = validaU()
class Usuario:
    
    def register_user(self, id: int, username: str, phone: int, email: str, password: str):
       
        if not isinstance(id, int) or id <= 0:
            return JSONResponse(content={"success": False, "message": "El ID debe ser un número entero positivo"}, status_code=400)
        if not username or username.strip() == "":
            return JSONResponse(content={"success": False, "message": "El nombre de usuario es obligatorio"}, status_code=400)
        if not isinstance(phone, int) or phone <= 0:
            return JSONResponse(content={"success": False, "message": "El teléfono debe ser un número válido"}, status_code=400)
        if not re.match(r"[^@]+@[^@]+\.[^@]+", email):
            return JSONResponse(content={"success": False, "message": "El correo electrónico no es válido"}, status_code=400)
        if not password or len(password) < 6:
            return JSONResponse(content={"success": False, "message": "La contraseña debe tener al menos 6 caracteres"}, status_code=400)

        if val.user_exist:
       
            query = """
                INSERT INTO usuarios (User_id, User_name, User_phone, User_mail, User_password) 
                VALUES (%s, %s, %s, %s, %s)
            """
            try:
                execute_query(query, (id, username, phone, email, password), commit=True)
                return JSONResponse(content={
                    "success": True,
                    "message": "Usuario registrado exitosamente"
                }, status_code=201)
            except Exception as e:
                print(f"Error en register_user: {e}")
                return JSONResponse(content={
                    "success": False,
                    "message": f"Error al registrar usuario: {e}"
                }, status_code=500)
        



    def update_user(self, id: int, username: str, phone: int, email: str, password: str):
       
        if not isinstance(id, int) or id <= 0:
            return JSONResponse(content={"success": False, "message": "El ID es inválido"}, status_code=400)
        if not username or username.strip() == "":
            return JSONResponse(content={"success": False, "message": "El nombre de usuario es obligatorio"}, status_code=400)
        if not re.match(r"[^@]+@[^@]+\.[^@]+", email):
            return JSONResponse(content={"success": False, "message": "Correo electrónico inválido"}, status_code=400)
        if not password or len(password) < 6:
            return JSONResponse(content={"success": False, "message": "La contraseña debe tener al menos 6 caracteres"}, status_code=400)

        query = """
            UPDATE usuarios 
            SET User_name = %s, User_phone = %s, User_mail = %s, User_password = %s 
            WHERE User_id = %s
        """
        try:
            rows = execute_query(query, (username, phone, email, password, id), commit=True)
            if rows == 0:
                return JSONResponse(content={
                    "success": False,
                    "message": "Usuario no encontrado"
                }, status_code=404)

            return JSONResponse(content={
                "success": True,
                "message": "Usuario actualizado exitosamente"
            }, status_code=200)
           
        except Exception as e:
            print(f"Error en update_user: {e}")
            return JSONResponse(content={
                "success": False,
                "message": "Error al actualizar usuario"
            }, status_code=500)


    def view_user(self, id: int):
        if not isinstance(id, int) or id <= 0:
            return JSONResponse(content={"success": False, "message": "ID inválido"}, status_code=400)

        query = "SELECT User_id, User_name, User_phone, User_mail, User_password FROM usuarios WHERE User_id = %s"
        try:
            user = execute_query(query, (id,), fetchone=True)
            if user:
                return JSONResponse(content={
                    "success": True,
                    "message": "Usuario encontrado",
                    "data": {
                        "id": user[0],
                        "username": user[1],
                        "phone": user[2],
                        "email": user[3],
                        "password": user[4]  
                    }
                }, status_code=200)
            else:
                return JSONResponse(content={"success": False, "message": "Usuario no encontrado"}, status_code=404)
        except Exception as e:
            print(f"Error en view_user: {e}")
            return JSONResponse(content={
                "success": False,
                "message": "Error al obtener usuario"
            }, status_code=500)
