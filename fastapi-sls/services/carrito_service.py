from db import execute_query
from services.producto_service import  verificar_cantidad


def verificar_carrito_activo(user_id: int):
        query_carrito = """
                SELECT Car_id 
                FROM carrito 
                WHERE User_id = %s AND estado = 'activo'
                LIMIT 1
            """
        result = execute_query(query_carrito, (user_id,), fetchone=True)
            
        if result:
            car_id = result[0]  #validamos que el carrito existe
        else:
            # 2. Crear un carrito nuevo
            insert_carrito = """
                INSERT INTO carrito (User_id, estado) VALUES (%s, 'activo')
            """
            car_id = execute_query( insert_carrito,(user_id,), commit=True,return_id=True)   
        return car_id

def obtener_carrito_usuario(user_id: int):
    query = """
        SELECT 
            u.User_name,
            c.Car_id,
            c.fecha_creacion,
            c.estado,
            p.Product_name AS nombre_producto,
            cd.Detalle_cantidad AS cantidad,
            p.Product_price AS precio_unitario,
            (cd.Detalle_cantidad * p.Product_price) AS subtotal
        FROM carrito c
        INNER JOIN usuarios u ON u.User_id = c.User_id
        INNER JOIN carrito_detalle cd ON cd.Car_id = c.Car_id
        INNER JOIN productos p ON cd.Product_id = p.Product_id
        WHERE c.User_id = %s AND c.estado = 'activo'
    """

    try:
        result = execute_query(query, (user_id,), fetchall=True)

        if not result:
            return {
                "success": False,
                "message": f"⚠️ El usuario {user_id} no tiene productos en el carrito"
            }

        # Datos generales del carrito (primer registro)
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
        return {
            "success": False,
            "message": "❌ Error al obtener los productos del carrito"
        }
        
        
def insertar_producto(car_id, product_id, cantidad, producto):
    
    try:
        query = """
            INSERT INTO carrito_detalle (Car_id, Product_id, Detalle_cantidad, precio_unitario)
            VALUES (%s, %s, %s, %s)
        """
        params = (car_id, product_id, cantidad, producto[3])

        detalle_id = execute_query(query, params, commit=True, return_id=True)

        return {
            "success": True,
            "message": f"✅ Producto {product_id} agregado al carrito (filas afectadas: {detalle_id})",
            "detalle_id": detalle_id
        }
    except Exception as e:
        return {
            "success": False,
            "message": f"❌ Error al insertar producto: {e}"
        } 
        
        
def eliminar_producto(car_id: int, product_id: int):
    """
    Elimina un producto del carrito de compras.
    :param car_id: ID del carrito
    :param product_id: ID del producto a eliminar
    """
    try:
        query = """
            DELETE FROM carrito_detalle
            WHERE Car_id = %s AND Product_id = %s
        """
        params = (car_id, product_id)
        rows_deleted = execute_query(query, params, commit=True)

        if rows_deleted > 0:
            return {
                "success": True,
                "message": f"🗑️ Producto {product_id} eliminado del carrito"
            }
        else:
            return {
                "success": False,
                "message": f"⚠️ El producto {product_id} no existe en el carrito"
            }

    except Exception as e:
        return {
            "success": False,
            "message": f"❌ Error al eliminar producto: {e}"
        }
        
        
def actualizar_cantidad(detalle_id: int, car_id: int, nueva_cantidad: int, product_id: int):
    # validar stock
    validacion = verificar_cantidad(product_id, nueva_cantidad)
    if not validacion["success"]:
        return validacion

    query_update = """
        UPDATE carrito_detalle
        SET Detalle_cantidad = %s
        WHERE Detalle_id = %s AND Car_id = %s
    """
    rows_affected = execute_query(query_update, (nueva_cantidad, detalle_id, car_id), commit=True)

    if rows_affected == 0:
        return {"success": False, "message": "No se pudo actualizar la cantidad"}

    return {"success": True, "message": f"Cantidad actualizada a {nueva_cantidad}"}
 

