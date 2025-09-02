from db import execute_query

class Login:
<<<<<<< HEAD:fastapi-sls/models/login/logic/login_consl.py

=======
    
>>>>>>> 9258571155c2a8e731a429f6add1910b70fe2989:fastapi-sls/models/login/login_class.py
    def login_user(username: str, password: str):
        query = "SELECT * FROM usuarios WHERE User_name = %s AND User_password = %s"
        try:
            result = execute_query(query, (username, password), fetchone=True)
            return result
        except Exception as e:
            print(f"Error en login_user: {e}")
            return None


