from models.carrito.carrito_entity import CarritoEntity, ActualizarCarrito
from db import execute_query

class CarritoClass:
    def agregar_producto(self, carrito: CarritoEntity):
        try:
            #Verificar si el usuario existe
            query_usuario = """
            SELECT User_id
            FROM usuarios
            WHERE User_id = %s
            LIMIT 1
            """
            
            usuario = execute_query(query_usuario, (carrito.user_id,), fetchone=True)
            
            if not usuario:
                return {
                    "success": False,
                    "message": f"El usuario con ID {carrito.user_id} no existe"
                }
            
            # 1. Revisar si el usuario ya tiene un carrito activo
            query_carrito = """
                SELECT Car_id 
                FROM carrito 
                WHERE User_id = %s AND estado = 'activo'
                LIMIT 1
            """
            result = execute_query(query_carrito, (carrito.user_id,), fetchone=True)

            if result:
                car_id = result[0]  #validamos que el carrito existe
            else:
                # 2. Crear un carrito nuevo
                insert_carrito = """
                    INSERT INTO carrito (User_id, estado) VALUES (%s, 'activo')
                """
                car_id = execute_query(
                    insert_carrito,
                    (carrito.user_id,),
                    commit=True,
                    return_id=True
                )

            # 3. Consultar precio del producto desde la tabla productos
            query_precio = "SELECT Product_price FROM productos WHERE Product_id = %s"
            result_precio = execute_query(query_precio, (carrito.product_id,), fetchone=True)

            if not result_precio:
                return {
                    "success": False,
                    "message": "El producto no existe"
                }

            precio_unitario = result_precio[0]

            # 4. Insertar producto en carrito_detalle
            insert_detalle = """
                INSERT INTO carrito_detalle (Car_id, Product_id, Detalle_cantidad, precio_unitario)
                VALUES (%s, %s, %s, %s)
            """
            params_detalle = (
                car_id,
                carrito.product_id,
                carrito.car_cantidad,
                precio_unitario
            )
            execute_query(insert_detalle, params_detalle, commit=True)

            return {
                "success": True,
                "message": "Producto agregado al carrito",
            }

        except Exception as e:
            print(f"Error al agregar producto: {e}")
            return {
                "success": False,
                "message": f"Error al agregar el producto al carrito: {str(e)}"
            }


    def obtener_carrito_usuario(self, User_id: int):
        query = """
            SELECT 
                u.User_name,
                c.Car_id,
                c.fecha_creacion,
                c.estado,
                p.product_name AS nombre_producto,
                cd.Detalle_cantidad AS cantidad,
                cd.precio_unitario AS precio_unitario,
                (cd.Detalle_cantidad * cd.precio_unitario) AS subtotal
            FROM carrito c
            INNER JOIN usuarios u ON u.User_id = c.User_id
            INNER JOIN carrito_detalle cd ON cd.Car_id = c.Car_id
            INNER JOIN productos p ON cd.Product_id = p.Product_id
            WHERE c.User_id = %s AND c.estado = 'activo'
        """
        try:
            result = execute_query(query, (User_id,), fetchall=True)

            if not result:
                return {"success": False, "message": "El carrito está vacío"}

            # Datos generales del carrito (tomamos del primer registro)
            user_name = result[0][0]
            car_id = result[0][1]
            fecha_creacion = result[0][2]
            estado = result[0][3]

            # Lista de productos
            productos = [
                {
                    "nombre_producto": row[4],
                    "cantidad": row[5],
                    "precio_unitario": f"${row[6]:,.0f}".replace(",", "."),
                    "subtotal": f"${row[7]:,.0f}".replace(",", ".")
                }
                for row in result
            ]

            # Total a pagar
            total_pagar = sum(row[7] for row in result)

            return {
                "success": True,
                "usuario": user_name,
                "carrito": {
                    "Car_id": car_id,
                    "fecha_creacion": str(fecha_creacion),
                    "estado": estado
                },
                "productos": productos,
                "total_pagar": f"${total_pagar:,.0f}".replace(",", ".")
            }

        except Exception as e:
            print(f"Error al obtener carrito: {e}")
            return {"success": False, "message": "Error al obtener los productos del carrito"}



    def eliminar_producto(self, detalle_id: int):
        try:
            query = """
                DELETE FROM carrito_detalle
                WHERE Detalle_id = %s
            """
            rows_affected = execute_query(query, (detalle_id,), commit=True)

            if rows_affected == 0:
                return {
                    "success": False,
                    "message": "El producto no fue encontrado en el carrito"
                }

            return {
                "success": True,
                "message": "Producto eliminado del carrito"
            }

        except Exception as e:
            print(f"Error al eliminar producto: {e}")
            return {
                "success": False,
                "message": f"Error al eliminar el producto del carrito: {str(e)}"
            }


    def actualizar_cantidad_producto(self, detalle_id: int, nueva_cantidad: int):
        try:
            # 1. Verificar si existe el detalle en el carrito
            query_check = "SELECT 1 FROM carrito_detalle WHERE Detalle_id = %s LIMIT 1"
            existe = execute_query(query_check, (detalle_id,), fetchone=True)

            if not existe:
                return {
                    "success": False,
                    "message": "Producto no encontrado, no se puede actualizar"
                }

            # 2. Si existe, actualizamos
            query_update = """
                UPDATE carrito_detalle
                SET Detalle_cantidad = %s
                WHERE Detalle_id = %s
            """
            rows_affected = execute_query(query_update, (nueva_cantidad, detalle_id), commit=True)

            if rows_affected == 0:
                return {
                    "success": False,
                    "message": "No se pudo actualizar la cantidad"
                }

            return {
                "success": True,
                "message": f"Cantidad actualizada a {nueva_cantidad}"
            }

        except Exception as e:
            print(f"Error al actualizar cantidad: {e}")
            return {
                "success": False,
                "message": f"Error al actualizar la cantidad: {str(e)}"
            }

            



