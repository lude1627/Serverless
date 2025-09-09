from db import execute_query

def verificar_usuario_existe(user_id: int, user_name: str):
    query = """
        SELECT User_id, User_name
        FROM usuarios
        WHERE User_id = %s
        LIMIT 1
    """
    usuario = execute_query(query, (user_id, user_name,), fetchone=True)

    if not usuario:
        return {
            "success": False,
            "message": f"❌ El usuario con ID {user_id} no existe"
        }
    
    return {
        "success": True,
        "message": f"✅ Usuario {user_id, user_name} encontrado"
    }
