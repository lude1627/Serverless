from db import execute_query

def verificar_usuario_existe(user_id: int):
    query = """
        SELECT User_id 
        FROM usuarios
        WHERE User_id = %s
        LIMIT 1
    """
    usuario = execute_query(query, (user_id,), fetchone=True)

    if not usuario:
        return {
            "success": False,
            "message": f"❌ El usuario con ID {user_id} no existe"
        }
    
    return {
        "success": True,
        "message": f"✅ Usuario {user_id} encontrado"
    }
