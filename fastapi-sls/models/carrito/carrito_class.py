from models.carrito.carrito_entity import CarritoEntity
from db import execute_query

<<<<<<< HEAD
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
=======
class CarritoClass:
    def agregar_producto(self, carrito: CarritoEntity):
        query = """
            INSERT INTO carrito (User_id, Product_id, Car_cantidad)
            VALUES (%s, %s, %s)
        """
        params = (carrito.user_id, carrito.product_id, carrito.cantidad)
        execute_query(query, params, commit=True)
        return {"success": True, "message": "Producto agregado al carrito"}

    def obtener_carrito_usuario(self, user_id: int):
        query = """
                SELECT 
                    c.Car_id,
                    c.User_id,
                    u.User_name AS nombre_usuario,
                    c.Product_id,
                    p.Product_name AS nombre_producto,
                    c.Car_cantidad,
                    p.Product_price AS precio_unitario,
                    (c.Car_cantidad * p.Product_price) AS subtotal,
                    c.Car_fecha_agregado
>>>>>>> 049f7d21d64083a8df79d284a8f43723b955141a
                FROM carrito c
                INNER JOIN usuarios u ON c.User_id = u.User_id
                INNER JOIN productos p ON c.Product_id = p.Product_id
                WHERE c.User_id = %s
        """
        result = execute_query(query, (user_id,), fetchall=True)
        
        result = [
            {
                "Car_id": row[0],
                # "User_id": row[1],
                "nombre_usuario": row[2],
                # "Product_id": row[3],
                "nombre_producto": row[4],
                "Car_cantidad": row[5],
                "precio_unitario": float(row[6]),
                "subtotal": float(row[7]),
                "Car_fecha_agregado": row[8].isoformat() if row[8] else None
            }
            for row in result
        ]
            
        return {"success": True, "data": result}


    def eliminar_producto(self, car_id: int):
        query = "DELETE FROM carrito WHERE Car_id = %s"
        execute_query(query, (car_id,), commit=True)
        return {"success": True, "message": "Producto eliminado del carrito"}


    def actualizar_cantidad(self, car_id: int, cantidad: int):
        query = "UPDATE carrito SET Car_cantidad = %s WHERE Car_id = %s"
        execute_query(query, (cantidad, car_id), commit=True)
        return {"success": True, "message": "Cantidad actualizada"}
