from db import execute_query
from fastapi.responses import JSONResponse

class Login:

    def login_user(username: str, password: str):
        query = "SELECT * FROM usuarios WHERE User_name = %s AND User_password = %s"
        try:
            user = execute_query(query, (username, password), fetchone=True)
            user_id = user[0]
            return JSONResponse(content={
                    "success": True,
                    "message": f"Bienvenid@ {username}",
                    "data": {"user_id": user_id}
                })
 
              
        except Exception as e:
            print(f"Error en login_user: {e}")
            return JSONResponse(content={
                    "success": False,
                    "message": "Usuario o contraseña incorrectos"
                })

