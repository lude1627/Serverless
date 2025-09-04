from models.carrito.carrito_entity import CarritoEntity
from db import execute_query

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
