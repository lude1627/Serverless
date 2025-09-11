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

        existe = usuario is not None and (usuario.get("User_id") if isinstance(usuario, dict) else usuario[0])

        return {
            "success": True,
            "existe": bool(existe),
            "message": f"✅ Usuario {user_id} encontrado" if existe else f"⚠️ Usuario {user_id} no existe"
        }
    except Exception as e:
        print("ERROR verificar_usuario_existe:", e)
        return {
            "success": False,
            "existe": False,
            "message": f"❌ Error al verificar usuario: {e}"
        }



