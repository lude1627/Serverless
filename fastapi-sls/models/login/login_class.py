from db import execute_query

class Login:
<<<<<<< HEAD
    
    def login_user(self, username: str, password: str):
=======

    def login_user(username: str, password: str):
>>>>>>> 7ecab891f2fd8ddbdc2c002bde903de2492407a0
        query = "SELECT * FROM usuarios WHERE User_name = %s AND User_password = %s"
        try:
            result = execute_query(query, (username, password), fetchone=True)
            return result
        except Exception as e:
            print(f"Error en login_user: {e}")
            return None


