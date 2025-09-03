from db import execute_query
from fastapi.responses import JSONResponse


class Usuario:
    
    def register_user(self, id: int, username: str, phone: int, email: str, password: str):
        query = """
            INSERT INTO usuarios (User_id, User_name, User_phone, User_mail, User_password) 
            VALUES (%s, %s, %s, %s, %s)
        """
        try:
            execute_query(query, (id, username, phone, email, password), commit=True)
            return JSONResponse(content={
                "success": True,
                "message": "Usuario registrado exitosamente"
            })
        except Exception as e:
            print(f"Error en register_user: {e}")
            return JSONResponse(content={
                "success": False,
                "message": f"Error al registrar usuario: {e}"
            })


    def update_user(self, id: int, username: str, phone: int, email: str, password: str):
        query = """
            UPDATE usuarios 
            SET User_name = %s, User_phone = %s, User_mail = %s, User_password = %s 
            WHERE User_id = %s
        """
        try:
            usuario = execute_query(query, (username, phone, email, password, id), commit=True)
            if not usuario:
                    return JSONResponse(content={
                        "success": True,
                        "message": "Usuario actualizado exitosamente"
                         })
            else:
                    return JSONResponse(content={
                            "success": False,
                            "message": "Error al actualizar usuario"
                        })
           
        except Exception as e:
            print(f"Error en update_user: {e}")
            return False


    def view_user(self, id: int):
        query = "SELECT * FROM usuarios WHERE User_id = %s"
        try:
            user= execute_query(query, (id,), fetchone=True)
            if user:
           
                        return JSONResponse(content={
                            "id": user[0],
                            "username": user[1],
                            "phone": user[2],
                            "email": user[3],
                            "password": user[4]
                        })
            else:
                     return JSONResponse(content={"error": "Usuario no encontrado"}, status_code=404)
        except Exception as e:
            print(f"Error en view_user: {e}")
            return None