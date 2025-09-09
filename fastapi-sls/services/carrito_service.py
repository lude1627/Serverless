from db import execute_query
from services.usuario_service import verificar_usuario_existe 
from services.carrito_service import  obtener_carrito_usuario


def verificar_carrito_activo(user_id: int):
    query = """
        SELECT Car_id
        FROM carrito
        WHERE User_id = %s AND estado = 'activo'
        LIMIT 1
    """
    carrito = execute_query(query, (user_id,), fetchone=True)

    if not carrito:
        return {
            "success": False,
            "message": f"⚠️ El usuario {user_id} no tiene un carrito activo"
        }
    
    return {
        "success": True,
        "message": "✅ Carrito activo encontrado",
        "car_id": carrito["Car_id"]
    }

def obtener_carrito_usuario(user_id: int):
    """
    Devuelve el carrito activo de un usuario con todos sus productos.
    """
    query = """
        SELECT 
            u.User_name,
            c.Car_id,
            c.fecha_creacion,
            c.estado,
            p.Product_name AS nombre_producto,
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
        result = execute_query(query, (user_id,), fetchall=True)

        if not result:
            return {
                "success": False,
                "message": f"⚠️ El usuario {user_id} no tiene productos en el carrito"
            }

        # Datos generales del carrito (primer registro)
        user_name = result[0]["User_name"]
        car_id = result[0]["Car_id"]
        fecha_creacion = result[0]["fecha_creacion"]
        estado = result[0]["estado"]

        # Lista de productos
        productos = [
            {
                "nombre_producto": row["nombre_producto"],
                "cantidad": row["cantidad"],
                "precio_unitario": f"${row['precio_unitario']:,.0f}".replace(",", "."),
                "subtotal": f"${row['subtotal']:,.0f}".replace(",", ".")
            }
            for row in result
        ]

        # Total a pagar
        total_pagar = sum(row["subtotal"] for row in result)

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
        
def eliminar_producto(detalle_id: int, user_id: int):
    """
    Elimina un producto del carrito de un usuario.
    """
    try:
        query = """
            DELETE FROM carrito_detalle
            WHERE Detalle_id = %s
        """
        rows_affected = execute_query(query, (detalle_id,), commit=True)

        if rows_affected == 0:
            return {
                "success": False,
                "message": "❌ El producto no fue encontrado en el carrito"
            }

        # 🔥 Carrito actualizado después de eliminar
        carrito_actualizado = obtener_carrito_usuario(user_id)

        return {
            "success": True,
            "message": "✅ Producto eliminado del carrito",
            "carrito": carrito_actualizado
        }

    except Exception as e:
        print(f"Error al eliminar producto: {e}")
        return {
            "success": False,
            "message": f"Error al eliminar el producto del carrito: {str(e)}"
        }
 

