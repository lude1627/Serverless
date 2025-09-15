from db import execute_query

def verificar_usuario_existe(user_cc: int):
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



