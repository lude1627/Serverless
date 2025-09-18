from db import execute_query
from fastapi.responses import JSONResponse
from models.login.login_entity import LoginModel
from services.usuario_service import ValidateU
val = ValidateU()
class Login:

    def login_user(self, data:LoginModel):
        query = "SELECT * FROM usuarios WHERE user_cc = %s AND user_password = %s and user_status = '1'"
        try:
            confirmacion= execute_query(query, (data.user_cc, data.password), fetchone=True)
            
            if confirmacion:
                resultado = val.verificar_user_type_por_password(data.password)
                user_type = resultado["user_type"]
                if user_type == 1:
                     return JSONResponse(content={
                            "success": True,
                            "message": "Bienvenido Admin",
                            "user_type": 1
                })
                else:
                    query_name = "SELECT user_name FROM usuarios WHERE user_cc = %s and user_type = '2'"
                    username = execute_query(query_name,(data.user_cc,),fetchone=True)
                    
                    nombre_usuario = username[0] if username else "Usuario"
                   
                    return JSONResponse(content={
                        "success": True,
                        "message": f"Bienvenid@: {nombre_usuario}",
                        "user_type": 2,
                        "user_cc": data.user_cc
                    })
            else:
                 return JSONResponse(content={
                                    "success": False,
                                    "message": "Usuario o contraseña incorrectos"
                                })
        except Exception as e:        
<<<<<<< HEAD
                print(f"Error en login_user: {e}")
                


 
     
=======
                print(f"Error en login_user: {e}")
>>>>>>> fa8a8bb2d2ff674690a3ef004684323889f786b1
