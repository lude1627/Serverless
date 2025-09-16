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
                    
                })
                else:
                    
                    query_name = "SELECT user_name FROM usuarios WHERE user_cc = %s and user_type = '2'"
                    username = execute_query(query_name,(data.user_cc,),fetchone=True)
                   
                    
                    return JSONResponse(content={
                         
                        "success": True,
                        "message": {"Bienvenid@": username},
                        "": {"Identificacion":data.user_cc}
                    })
                    
            else:
                 return JSONResponse(content={
                                    "success": False,
                                    "message": "Usuario o contraseña incorrectos"
                                })

        except Exception as e:
                           
                print(f"Error en login_user: {e}")
                


 
     