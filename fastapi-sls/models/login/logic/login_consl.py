from db import execute_query

class Login:
    @staticmethod
    def login_user(username: str, password: str):
        query = "SELECT * FROM usuarios WHERE User_name = %s AND User_password = %s"
        try:
            result = execute_query(query, (username, password), fetchone=True)
            return result
        except Exception as e:
            print(f"Error en login_user: {e}")
            return None


