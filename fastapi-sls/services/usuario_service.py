from db import execute_query


class ValidateU:
    def verificar_usuario_existe(self, user_cc: int):
        try:
            
            
            query = """
                SELECT user_cc
                FROM usuarios
                WHERE user_cc = %s and user_status = '1'
                LIMIT 1
            """
            usuario = execute_query(query, (user_cc,), fetchone=True)
            
        

            existe = usuario is not None and (usuario.get("User_cc") if isinstance(usuario, dict) else usuario[0])
        
            return {
                "success": True,
                "existe": bool(existe),
                "message": f"✅ Usuario {user_cc} encontrado" if existe else f"⚠️ Usuario {user_cc} no existe"
            }
        except Exception as e:
            print("ERROR verificar_usuario_existe:", e)
            return {
                "success": False,
                "existe": False,
                "message": f"❌ Error al verificar usuario: {e}"
            }

    def verificar_user_type(self, user_cc: int, password: str):
        try:
            query = """
                SELECT user_type
                FROM usuarios
                WHERE user_cc = %s AND user_password = %s
                LIMIT 1
            """
            result = execute_query(query, params=(user_cc, password), fetchone=True)

            if result:
                user_type = result[0]
                return {
                    "success": True,
                    "user_type": user_type,
                    "message": (
                        "✅ Usuario administrador (user_type=1)"
                        if user_type == 1
                        else "👤 Usuario cliente (user_type=2)"
                    )
                }
            else:
                return {
                    "success": False,
                    "user_type": None,
                    "message": "❌ Usuario o contraseña incorrectos."
                }

        except Exception as e:
            return {
                "success": False,
                "user_type": None,
                "message": f"⚠️ Error al verificar usuario: {e}"
            }



