from fastapi.responses import JSONResponse
from db import execute_query
from models.carrito.carrito_entity import CarritoEntity

class Carrito:

    # ✅ Agregar producto al carrito
    def agregar_producto  (self, carrito: CarritoEntity):
        user_id = carrito.user_id
        product_id = carrito.product_id
        cantidad = carrito.cantidad

        query = "INSERT INTO carrito (user_id, product_id, cantidad) VALUES (%s, %s, %s)"
        print("=========entro aqui========")

        try:
            execute_query(query, (user_id, product_id, cantidad), commit=True)
            print("===ejecuto el query======")
            return JSONResponse(content={
                "success": True,
                "message": "Producto agregado al carrito"
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
            execute_query(query_update, (cantidad, id), commit=True)

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
            execute_query(query_delete, (id,), commit=True)

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
                SELECT c.id, p.Product_name, p.Product_price, c.cantidad, 
                       (p.Product_price * c.cantidad) as total
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
