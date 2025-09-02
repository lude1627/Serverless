from db import execute_query
def register_user(id: int, username: str, phone: int, email: str, password: str):
    query = """
        INSERT INTO usuarios (User_id, User_name, User_phone, User_mail, User_password) 
        VALUES (%s, %s, %s, %s, %s)
    """
    try:
        execute_query(query, (id, username, phone, email, password), commit=True)
        return True
    except Exception as e:
        print(f"Error en register_user: {e}")
        return False


def update_user(id: int, username: str, phone: int, email: str, password: str):
    query = """
        UPDATE usuarios 
        SET User_name = %s, User_phone = %s, User_mail = %s, User_password = %s 
        WHERE User_id = %s
    """
    try:
        execute_query(query, (username, phone, email, password, id), commit=True)
        return True
    except Exception as e:
        print(f"Error en update_user: {e}")
        return False


def view_user(id: int):
    query = "SELECT * FROM usuarios WHERE User_id = %s"
    try:
        result = execute_query(query, (id,), fetchone=True)
        return result
    except Exception as e:
        print(f"Error en view_user: {e}")
        return None