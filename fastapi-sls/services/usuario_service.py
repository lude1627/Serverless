from db import execute_query

def verificar_usuario_existe(user_cc: int):
    try:
        print("DEBUG verificar_usuario_existe - user_cc:", user_cc, type(user_cc))
        
        query = """
            SELECT User_cc 
            FROM usuarios
            WHERE User_cc = %s
            LIMIT 1
        """
        usuario = execute_query(query, (user_cc,), fetchone=True)
        
        print("DEBUG resultado consulta:", usuario)

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



