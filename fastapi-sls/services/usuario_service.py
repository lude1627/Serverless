from db import execute_query

def verificar_usuario_existe(user_id: int):
    try:
        print("DEBUG verificar_usuario_existe - user_id:", user_id, type(user_id))
        
        query = """
            SELECT User_id 
            FROM usuarios
            WHERE User_id = %s
            LIMIT 1
        """
        usuario = execute_query(query, (user_id,), fetchone=True)
        
        print("DEBUG resultado consulta:", usuario)

        return {
            "success": True,
            "existe": bool(usuario),
            "message": f"✅ Usuario {user_id} encontrado" if usuario else f"⚠️ Usuario {user_id} no existe"
        }
    except Exception as e:
        print("ERROR verificar_usuario_existe:", e)
        return {
            "success": False,
            "existe": False,
            "message": f"❌ Error al verificar usuario: {e}"
        }


