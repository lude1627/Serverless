from db import execute_query
from fastapi.responses import JSONResponse
from models.user.user_entity import RegisterModel, UpdateUserModel, AdminUpdateUserModel
from services.usuario_service import ValidateU
import re

val = ValidateU()

class Usuario:
    
    def register_user(self, data: RegisterModel):
       
        if not isinstance(data.user_cc, int) or data.user_cc <= 0:
            return JSONResponse(content={"success": False, "message": "El ID debe ser un número entero positivo"}, status_code=400)
        if not data.username or data.username.strip() == "":
            return JSONResponse(content={"success": False, "message": "El nombre de usuario es obligatorio"}, status_code=400)
        if not isinstance(data.phone, int) or data.phone <= 0:
            return JSONResponse(content={"success": False, "message": "El teléfono debe ser un número válido"}, status_code=400)
        if not re.match(r"[^@]+@[^@]+\.[^@]+", data.email):
            return JSONResponse(content={"success": False, "message": "El correo electrónico no es válido"}, status_code=400)
        if not data.password or len(data.password) < 6:
            return JSONResponse(content={"success": False, "message": "La contraseña debe tener al menos 6 caracteres"}, status_code=400)

        # Check if user exists
        resultado_usuario = val.verificar_usuario_existe(data.user_cc)
        if resultado_usuario["existe"]:
            return JSONResponse(content={
                "success": False,
                "message": f"El usuario con el ID {data.user_cc} ya existe"
            }, status_code=400)
            
        resultado = val.verificar_user_type_por_password(data.password)
        user_type = resultado["user_type"]
              
        query = """
                INSERT INTO usuarios (user_cc, user_type, user_name, user_phone, user_mail, user_password, user_status) 
                VALUES (%s, %s, %s, %s, %s, %s, '1')
            """
            
        try:
            execute_query(query, (data.user_cc, user_type, data.username, data.phone, data.email, data.password), commit=True)
            return JSONResponse(content={
                "success": True,
                "message": "Usuario registrado exitosamente"
            }, status_code=201)
        except Exception as e:
            print(f"Error en register_user: {e}")
            return JSONResponse(content={
                "success": False,
                "message": f"Error al registrar usuario: {e}"
            }, status_code=500)
        

    def update_user(self, data: UpdateUserModel):
       
        if not isinstance(data.user_cc, int) or data.user_cc <= 0:
            return JSONResponse(content={"success": False, "message": "El ID es inválido"}, status_code=400)
        if not data.username or data.username.strip() == "":
            return JSONResponse(content={"success": False, "message": "El nombre de usuario es obligatorio"}, status_code=400)
        if not re.match(r"[^@]+@[^@]+\.[^@]+", data.email):
            return JSONResponse(content={"success": False, "message": "Correo electrónico inválido"}, status_code=400)
      

        query = """
            UPDATE usuarios 
            SET user_name = %s, user_phone = %s, user_mail = %s
            WHERE user_cc = %s or user_id = %s
        """
        try:
            rows = execute_query(query, (data.username, data.phone, data.email, data.user_cc), commit=True)
            if rows == 0:
                return JSONResponse(content={
                    "success": False,
                    "message": "Usuario no encontrado"
                }, status_code=404)

            return JSONResponse(content={
                "success": True,
                "message": "Usuario actualizado exitosamente"
            }, status_code=200)
            
        except Exception as e:
            print(f"Error en update_user: {e}")
            return JSONResponse(content={
                "success": False,
                "message": "Error al actualizar usuario"
            }, status_code=500)
            

    def view_user(self, user_cc: int = None, user_id: int = None):
        try:
            # Validación: al menos uno de los dos debe venir
            if user_cc is None and user_id is None:
                return JSONResponse(content={"success": False, "message": "Debe proporcionar user_cc o user_id"}, status_code=400)

            # Construcción dinámica de query y parámetros
            if user_cc:
                query = """
                    SELECT user_id, user_cc, user_name, user_phone, user_mail, user_password
                    FROM usuarios WHERE user_cc = %s
                """
                params = (user_cc,)
            else:
                query = """
                    SELECT user_id, user_cc, user_name, user_phone, user_mail, user_password
                    FROM usuarios WHERE user_id = %s
                """
                params = (user_id,)

            # Ejecución de la consulta
            user = execute_query(query, params, fetchone=True)

            if user:
                return JSONResponse(content={
                    "success": True,
                    "message": "Usuario encontrado",
                    "data": {
                        "user_id": user[0],
                        "user_cc": user[1],
                        "username": user[2],
                        "phone": user[3],
                        "email": user[4],
                    }
                }, status_code=200)
            else:
                return JSONResponse(content={
                    "success": False,
                    "message": "Usuario no encontrado"
                }, status_code=404)

        except Exception as e:
            print(f"Error en view_user: {e}")
            return JSONResponse(content={
                "success": False,
                "message": "Error al obtener usuario"
            }, status_code=500)

            
    #Exclusivo para acciones del admin 
    def view_all_users(self):
        query = """
            SELECT user_id,user_cc, user_type, user_name, user_phone, user_mail, user_status 
            FROM usuarios 
            ORDER BY user_cc
        """
        
        try:
            users = execute_query(query, fetchall=True)
            if users:
                user_list = []
                for user in users:
                    user_list.append({
                        "user_id": user[0],
                        "user_cc": user[1],
                        "user_type": user[2],
                        "username": user[3],
                        "phone": user[4],
                        "email": user[5],
                        "status": user[6]
                    })
                return JSONResponse(content={
                    "success": True,
                    "data": user_list
                   }, status_code=200)
            else:
                return JSONResponse(content={
                    "success": True,
                    "data": [],
                    "message": "No hay usuarios registrados"
                }, status_code=200)
        except Exception as e:
            print(f"Error en view_all_users: {e}")
            return JSONResponse(content={
                "success": False,
                "message": "Error al obtener usuarios"
            }, status_code=500)
                
                
    def admin_update_user(self, data: AdminUpdateUserModel):
        # Validation
        if not isinstance(data.user_cc, int) or data.user_cc <= 0:
            return JSONResponse(content={"success": False, "message": "El ID es inválido"}, status_code=400)
        if not data.username or data.username.strip() == "":
            return JSONResponse(content={"success": False, "message": "El nombre de usuario es obligatorio"}, status_code=400)
        if not re.match(r"[^@]+@[^@]+\.[^@]+", data.email):
            return JSONResponse(content={"success": False, "message": "Correo electrónico inválido"}, status_code=400)
        if not isinstance(data.phone, int) or data.phone <= 0:
            return JSONResponse(content={"success": False, "message": "El teléfono debe ser un número válido"}, status_code=400)
        
        # Check if user exists first
        check_query = """
        SELECT user_id 
        FROM usuarios 
        WHERE user_id = %s
        """
        try:
            existing_user = execute_query(check_query, (data.user_id,), fetchone=True)
            if not existing_user:
                return JSONResponse(content={
                    "success": False,
                    "message": "Usuario no encontrado"
                }, status_code=404)
        except Exception as e:
            print(f"Error checking user existence: {e}")
            return JSONResponse(content={
                "success": False,
                "message": "Error al verificar usuario"
            }, status_code=500)
        
        # Update query - password is optional for admin updates
        if data.password:
            query = """
                UPDATE usuarios 
                SET user_cc = %s, user_name = %s, user_phone = %s, user_mail = %s, user_type = %s, user_status = %s, user_password = %s
                WHERE user_id = %s
            """
            params = (data.user_cc, data.username, data.phone, data.email, data.user_type, data.user_status, data.password, data.user_id)
        else:
            query = """
                UPDATE usuarios 
                SET user_cc = %s, user_name = %s, user_phone = %s, user_mail = %s, user_type = %s, user_status = %s
                WHERE user_id = %s
            """
            params = (data.user_cc, data.username, data.phone, data.email, data.user_type, data.user_status, data.user_id)
            
        try:
            rows_affected = execute_query(query, params, commit=True)
            
            if rows_affected == 0:
                return JSONResponse(content={
                    "success": False,
                    "message": "No se pudo actualizar el usuario"
                }, status_code=400)
            
            return JSONResponse(content={
                "success": True, 
                "message": "Usuario actualizado correctamente"
            }, status_code=200)
            
        except Exception as e:
            print(f"Error en admin_update_user: {e}")
            return JSONResponse(content={
                "success": False, 
                "message": f"Error al actualizar usuario: {str(e)}"
            }, status_code=500)
            
            
            
    def admin_register_user(self, data: AdminUpdateUserModel):
        # Validation
        if not isinstance(data.user_cc, int) or data.user_cc <= 0:
            return JSONResponse(content={"success": False, "message": "El ID debe ser un número entero positivo"}, status_code=400)
        if not data.username or data.username.strip() == "":
            return JSONResponse(content={"success": False, "message": "El nombre de usuario es obligatorio"}, status_code=400)
        if not isinstance(data.phone, int) or data.phone <= 0:
            return JSONResponse(content={"success": False, "message": "El teléfono debe ser un número válido"}, status_code=400)
        if not re.match(r"[^@]+@[^@]+\.[^@]+", data.email):
            return JSONResponse(content={"success": False, "message": "El correo electrónico no es válido"}, status_code=400)
        if data.password and len(data.password) < 6:
            return JSONResponse(content={"success": False, "message": "La contraseña debe tener al menos 6 caracteres"}, status_code=400)
        if data.user_type not in [1, 2]:
            return JSONResponse(content={"success": False, "message": "Tipo de usuario inválido"}, status_code=400)
        if data.user_status not in [0, 1]:
            return JSONResponse(content={"success": False, "message": "Estado de usuario inválido"}, status_code=400)

        # Check if user exists
        resultado_usuario = val.verificar_usuario_existe(data.user_cc)
        if resultado_usuario["existe"]:
            return JSONResponse(content={
                "success": False,
                "message": f"El usuario con el ID {data.user_cc} ya existe"
            }, status_code=400)
            
        # Use provided password or generate default if not provided
        password = data.password if data.password else "123456"  # Default password for admin-created users
              
        query = """
                INSERT INTO usuarios (user_cc, user_type, user_name, user_phone, user_mail, user_password, user_status) 
                VALUES (%s, %s, %s, %s, %s, %s, %s)
            """
            
        try:
            execute_query(query, (data.user_cc, data.user_type, data.username, data.phone, data.email, password, data.user_status), commit=True)
            return JSONResponse(content={
                "success": True,
                "message": "Usuario registrado exitosamente por el administrador"
            }, status_code=201)
        except Exception as e:
            print(f"Error en admin_register_user: {e}")
            return JSONResponse(content={
                "success": False,
                "message": f"Error al registrar usuario: {e}"
            }, status_code=500)