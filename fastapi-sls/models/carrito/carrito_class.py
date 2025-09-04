from fastapi.responses import JSONResponse
from db import execute_query
from models.carrito.carrito_entity import CarritoEntity

class Carrito:

    def agregar_producto(self, carrito: CarritoEntity):
        try:
            # Verificar si ya existe ese producto en el carrito del usuario
            query_check = "SELECT Car_id, Car_cantidad FROM carrito WHERE user_id = %s AND product_id = %s"
            existente = execute_query(query_check, (carrito.user_id, carrito.product_id), fetchone=True)

            if existente:
                # Si existe, solo actualizamos cantidad
                query_update = "UPDATE carrito SET Car_cantidad = Car_cantidad + %s WHERE Car_id = %s"
                execute_query(query_update, (carrito.cantidad, existente[0]), commit=True)
                return JSONResponse(content={
                    "success": True,
                    "message": f"Cantidad actualizada en el carrito {e}"
                }, status_code=200)

            # Si no existe, insertamos nuevo registro
            query_insert = "INSERT INTO carrito (user_id, product_id, Car_cantidad) VALUES (%s, %s, %s)"
            execute_query(query_insert, (carrito.user_id, carrito.product_id, carrito.cantidad), commit=True)

            return JSONResponse(content={
                "success": True,
                "message": f"Producto agregado al carrito {e}"
            }, status_code=201)

        except Exception as e:
            return JSONResponse(content={
                "success": False,
                "message": f"Error: {str(e)}"
            }, status_code=400)
            
            
            
            # ✅ Actualizar cantidad de un producto en el carrito
    def actualizar_cantidad(self, id: int, cantidad: int):
        try:
            query_update = "UPDATE carrito SET cantidad = %s WHERE id = %s"
            result = execute_query(query_update, (cantidad, id), commit=True)

            if result is None:  # si no se encontró registro
                return JSONResponse(content={
                    "success": False,
                    "message": "No se encontró el producto en el carrito"
                }, status_code=404)

            return JSONResponse(content={
                "success": True,
                "message": "Cantidad actualizada correctamente"
            }, status_code=200)

        except Exception as e:
            return JSONResponse(content={
                "success": False,
                "message": f"Error: {str(e)}"
            }, status_code=400)
            
            
            # ✅ Eliminar un producto del carrito
    def eliminar_producto(self, id: int):
        try:
            query_delete = "DELETE FROM carrito WHERE id = %s"
            result = execute_query(query_delete, (id,), commit=True)

            if result is None:  # si no se encontró registro
                return JSONResponse(content={
                    "success": False,
                    "message": "No se encontró el producto en el carrito"
                }, status_code=404)

            return JSONResponse(content={
                "success": True,
                "message": "Producto eliminado del carrito"
            }, status_code=200)

        except Exception as e:
            return JSONResponse(content={
                "success": False,
                "message": f"Error: {str(e)}"
            }, status_code=400)
            
            
             # ✅ Obtener todos los productos del carrito de un usuario
    def obtener_carrito_usuario(self, user_id: int):
        try:
            query_select = """
                SELECT c.id, p.Product_name, p.Product_price, c.cantidad, (p.Product_price * c.cantidad) as total
                FROM carrito c
                INNER JOIN productos p ON c.product_id = p.Product_id
                WHERE c.user_id = %s
            """
            items = execute_query(query_select, (user_id,), fetchall=True)

            if not items:
                return JSONResponse(content={
                    "success": True,
                    "carrito": [],
                    "message": "El carrito está vacío"
                }, status_code=200)

            return JSONResponse(content={
                "success": True,
                "carrito": [
                    {
                        "carrito_id": item[0],
                        "producto": item[1],
                        "precio_unitario": item[2],
                        "cantidad": item[3],
                        "total": item[4]
                    } for item in items
                ]
            }, status_code=200)

        except Exception as e:
            return JSONResponse(content={
                "success": False,
                "message": f"Error: {str(e)}"
            }, status_code=400)
