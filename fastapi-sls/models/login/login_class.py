from db import execute_query
from fastapi.responses import JSONResponse

class Login:
    def login_user(self, username: str, password: str):
        query = "SELECT * FROM usuarios WHERE User_name = %s AND User_password = %s"
        try:
            user = execute_query(query, (username, password), fetchone=True)

            if user:
                user_id = user[0]   # OJO: depende de tu tabla, ajusta si no es el ID
                return JSONResponse(content={
                    "success": True,
                    "message": f"Bienvenid@ {username}",
                    "user_id": user_id
                })
            else:
                return JSONResponse(content={
                    "success": False,
                    "message": "Usuario o contraseña incorrectos"
                })

        except Exception as e:
            print(f"Error en login_user: {e}")
            return JSONResponse(content={
                "success": False,
                "message": "Error interno en el servidor"
            })

