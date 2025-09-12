from db import execute_query
from services.usuario_service import  verificar_usuario_existe


def verificar_carrito_activo(user_cc: int):
    try:
        # Verificar si el usuario existe antes de crear o consultar carrito
        usuario = verificar_usuario_existe(user_cc)
        if not usuario["existe"]:
            return {
                "success": False,
                "message": f"❌ No se puede crear carrito porque el usuario {user_cc} no existe"
            }
        
        # Buscar carrito activo
        query = """
            SELECT Car_id
            FROM carrito
            WHERE User_cc = %s AND estado = '1'
            LIMIT 1
        """
        carrito = execute_query(query, (user_cc,), fetchone=True)
        print("2")
        if not carrito:
            # Si no existe carrito, lo creamos
            query_insert = """
                INSERT INTO carrito (User_cc, fecha_creacion, estado)
                VALUES (%s, NOW(), '1')
            """
            execute_query(query_insert, (user_cc,), commit=True, return_id=True)


            car_id = execute_query(query, (user_cc,), fetchone=True)

            query = """
            SELECT Car_id
            FROM carrito
            WHERE User_cc = %s AND estado = '1'
            LIMIT 1
        """
            print("llego 4")
            return {
                "success": True,
                "message": f"🛒 Carrito creado para el usuario {user_cc}",
                "car_id": car_id[0]
            }
        print(car_id)
        # Si ya existe, devolver el ID
        return {
            "success": True,
            "message": "✅ Carrito activo encontrado",
            "car_id": carrito[0]
        }
        
    except Exception as e:
        return {
            "success": False,
            "message": f"❌ Error al verificar/crear carrito: {str(e)}"
        }


def obtener_carrito_usuario(user_cc: int):
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
        INNER JOIN usuarios u ON u.User_cc = c.User_cc
        INNER JOIN carrito_detalle cd ON cd.Car_id = c.Car_id
        INNER JOIN productos p ON cd.Product_id = p.Product_id
        WHERE c.User_cc = %s AND c.estado = '1'
    """

    try:
        result = execute_query(query, (user_cc,), fetchall=True)

        if not result:
            return {
                "success": False,
                "message": f"⚠️ El usuario {user_cc} no tiene productos en el carrito"
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

 
def eliminar_producto(detalle_id: int, car_id: int):
    
    try:
        query = """
            DELETE FROM carrito_detalle
            WHERE Detalle_id = %s AND Car_id = %s
        """
        params = (detalle_id, car_id)
        rows_deleted = execute_query(query, params, commit=True)

        if rows_deleted:
            return {
                "success": True,
                "message": f"🗑️ Producto {detalle_id} eliminado del carrito"
            }
        else:
            return {
                "success": False,
                "message": f"⚠️ El producto {detalle_id} no existe en el carrito {car_id}"
            }

    except Exception as e:
        print(f"❌ Error en eliminar_producto: {e}")
        return {
            "success": False,
            "message": f"❌ Error al eliminar producto: {e}"
        }


def finalizar_compra(car_id: int):
    # 1. Verificar carrito
    query_carrito = """
        SELECT Car_id, estado
        FROM carrito
        WHERE Car_id = %s and estado = 1
    """
    carrito = execute_query(query_carrito, (car_id,), fetchone=True)

    if not carrito:
        return {"success": False, "message": f"❌ Carrito {car_id} no encontrado"}

    if carrito["estado"] == 0:
        return {"success": False, "message": "⚠️ Este carrito ya fue cerrado"}

    # 2. Cerrar carrito
    query_update = """
        UPDATE carrito
        SET estado = 0
        WHERE Car_id = %s
    """
    execute_query(query_update, (car_id,))

    return {"success": True, "message": f"✅ Carrito {car_id} finalizado correctamente"}

    
    
