from models.carrito.carrito_entity import CarritoEntity, CarritoUpdate
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

    def obtener_carrito_usuario(self, User_id: int):
        query = """
            SELECT 
                c.Car_id, p.product_name AS nombre_producto, c.Car_cantidad AS cantidad, p.product_price AS precio_unitario, (c.Car_cantidad * p.product_price) AS subtotal
            FROM carrito c
            INNER JOIN productos p ON c.Product_id = p.Product_id
            WHERE c.User_id = %s
        """
        try:
            result = execute_query(query, (User_id,), fetchall=True)

            if not result:  
                return {"success": False, "message": "El carrito está vacío"}

            
            data = [
                {
                    "Car_id": row[0],
                    "nombre_producto": row[1],
                    "cantidad": row[2],
                    "precio_unitario": f"${row[3]:,.0f}".replace(",", "."),
                    "subtotal": f"${row[4]:,.0f}".replace(",", ".")
                }
                for row in result
            ]

            return {"success": True, "data": data}

        except Exception as e:
            print(f"Error al obtener carrito: {e}")
            return {"success": False, "message": "Error al obtener los productos del carrito"}



    def eliminar_producto(self, Car_id: int):
        query = "DELETE FROM carrito WHERE Car_id = %s"
        execute_query(query, (Car_id,), commit=True)
        return {"success": True, "message": "Producto eliminado del carrito"}


    def actualizar_cantidad(self, Car_id, Car_cantidad: int):
        query = "UPDATE carrito SET Car_cantidad = %s WHERE Car_id = %s"
    
        try: 
            result = execute_query(query, (Car_id, Car_cantidad), commit=True)
        except Exception as e:
            print(f"Error al actualizar cantidad: {e}")
            return {"success": False, "message": "Error al actualizar la cantidad"}
        
        if result == 0:  # Si no se afectó ninguna fila
            return {"success": False, "message": "Producto no encontrado en el carrito"}
        
        return {"success": True, "message": "Cantidad actualizada"}

