from db import execute_query
from fastapi.responses import JSONResponse
from models.login.login_entity import LoginModel

class Login:

    def login_user(self, data: LoginModel):
        try:
            # 🔑 Traemos user_type y user_name en la misma consulta
            query = """
                SELECT user_type, user_name
                FROM usuarios
                WHERE user_cc = %s AND user_password = %s
                LIMIT 1
            """
            result = execute_query(query, (data.user_cc, data.password), fetchone=True)

            if not result:
                return JSONResponse(content={
                    "success": False,
                    "message": "Usuario o contraseña incorrectos"
                })

            user_type, user_name = result
            user_type = int(user_type)  # Aseguramos que sea número

            if user_type == 1:
                # ✅ Admin
                return JSONResponse(content={
                    "success": True,
                    "message": "Bienvenido Admin",
                    "user_type": 1,
                    "user_cc": data.user_cc
                })
            elif user_type == 2:
                # ✅ Cliente
                return JSONResponse(content={
                    "success": True,
                    "message": f"Bienvenid@: {user_name or 'Usuario'}",
                    "user_type": 2,
                    "user_cc": data.user_cc
                })
            else:
                return JSONResponse(content={
                    "success": False,
                    "message": f"Tipo de usuario desconocido ({user_type})"
                })

        except Exception as e:
            print(f"Error en login_user: {e}")
            return JSONResponse(content={
                "success": False,
                "message": f"Error en login: {e}"
            }, status_code=500)
