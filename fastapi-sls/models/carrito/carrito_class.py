from fastapi.responses import JSONResponse
from db import execute_query
from models.carrito.carrito_entity import CarritoEntity

class Carrito:

    def agregar_producto(self, carrito: CarritoEntity):
        try:
            # Verificar si ya existe ese producto en el carrito del usuario
            query_check = "SELECT id, cantidad FROM carrito WHERE user_id = %s AND product_id = %s"
            existente = execute_query(query_check, (carrito.user_id, carrito.product_id), fetchone=True)

            if existente:
                # Si existe, solo actualizamos cantidad
                query_update = "UPDATE carrito SET cantidad = cantidad + %s WHERE id = %s"
                execute_query(query_update, (carrito.cantidad, existente[0]), commit=True)
                return JSONResponse(content={
                    "success": True,
                    "message": "Cantidad actualizada en el carrito"
                }, status_code=200)

            # Si no existe, insertamos nuevo registro
            query_insert = "INSERT INTO carrito (user_id, product_id, cantidad) VALUES (%s, %s, %s)"
            execute_query(query_insert, (carrito.user_id, carrito.product_id, carrito.cantidad), commit=True)

            return JSONResponse(content={
                "success": True,
                "message": "Producto agregado al carrito"
            }, status_code=201)

        except Exception as e:
            return JSONResponse(content={
                "success": False,
                "message": f"Error: {str(e)}"
            }, status_code=400)
