from db import execute_query
from services.usuario_service import ValidateU

val = ValidateU()
def verificar_carrito_activo(user_cc: int):
    try:
        # Verificar si el usuario existe antes de crear o consultar carrito
        usuario = val.verificar_usuario_existe(user_cc)
        if not usuario["existe"]:
            return {
                "success": False,
                "message": f"❌ No se puede crear carrito porque el usuario {user_cc} no existe"
            }
        
        # Buscar carrito activo
        query = """
            SELECT Car_id
            FROM carrito
            WHERE user_cc = %s AND estado = '1'
            LIMIT 1
        """
        carrito = execute_query(query, (user_cc,), fetchone=True)
    
        if carrito:

            # Si ya existe, devolver el ID
            return {
                "success": True,
                "message": "✅ Carrito activo encontrado",
                "car_id": carrito[0]
            }
    
        # Si no existe carrito, lo creamos
        query_insert = """
            INSERT INTO carrito (user_cc, fecha_creacion, estado)
            VALUES (%s, NOW(), '1')
        """
        execute_query(query_insert, (user_cc,), commit=True, return_id=True)

        query = """
            SELECT car_id
            FROM carrito
            WHERE user_cc = %s AND estado = '1'
            LIMIT 1
        """
        car_id = execute_query(query, (user_cc,), fetchone=True)
        
        print(car_id)
        return {
            "success": True,
            "message": f"🛒 Carrito creado para el usuario {user_cc}",
            "car_id": car_id[0]
        }
        
        
        
    except Exception as e:
        return {
            "success": False,
            "message": f"❌ Error al verificar/crear carrito: {str(e)}"
        }


def obtener_todos_carritos():
    query = """
        SELECT 
            c.car_id,
            u.user_cc,
            u.user_name,
            c.fecha_creacion,
            c.estado,
            SUM(cd.detalle_cantidad * p.product_price) AS total
        FROM carrito c
        INNER JOIN usuarios u ON c.user_cc = u.user_cc
        LEFT JOIN carrito_detalle cd ON c.car_id = cd.car_id
        LEFT JOIN productos p ON cd.product_id = p.product_id
        GROUP BY c.car_id, u.user_cc, u.user_name, c.fecha_creacion, c.estado
        ORDER BY c.fecha_creacion DESC
    """
    try:
        carritos = execute_query(query, fetchall=True)
        if not carritos:
            return {
                "success": False,
                "message": "⚠️ No hay carritos disponibles"
            }

        lista_carritos = []
        for row in carritos:
            lista_carritos.append({
                "car_id": row[0],
                "user_cc": row[1],
                "user_name": row[2],
                "fecha_creacion": row[3].strftime("%Y-%m-%d"),
                "estado": row[4],
                "total": f"${row[5]:,.0f}".replace(",", ".") if row[5] is not None else "$0"
            })

        return {
            "success": True,
            "data": lista_carritos
        }

    except Exception as e:
        print(f"Error al obtener todos los carritos: {e}")
        return {
            "success": False,
            "message": "❌ Error al obtener los carritos"
        }
def obtener_carritos_user(user_cc: int):
    query = """
        SELECT 
            c.car_id,
            u.user_cc,
            u.user_name,
            c.fecha_creacion,
            c.estado,
            SUM(cd.detalle_cantidad * p.product_price) AS total
        FROM carrito c
        INNER JOIN usuarios u ON c.user_cc = u.user_cc
        LEFT JOIN carrito_detalle cd ON c.car_id = cd.car_id
        LEFT JOIN productos p ON cd.product_id = p.product_id
        WHERE u.user_cc = %s
        GROUP BY c.car_id, u.user_cc, u.user_name, c.fecha_creacion, c.estado
        ORDER BY c.fecha_creacion DESC 
    """
    try:
        carritos = execute_query(query,(user_cc,), fetchall=True)
        if not carritos:
            return {
                "success": False,
                "message": "⚠️ No hay carritos disponibles"
            }

        lista_carritos = []
        for row in carritos:
            lista_carritos.append({
                "car_id": row[0],
                "user_cc": row[1],
                "user_name": row[2],
                "fecha_creacion": row[3].strftime("%Y-%m-%d"),
                "estado": row[4],
                "total": f"${row[5]:,.0f}".replace(",", ".") if row[5] is not None else "$0"
            })

        return {
            "success": True,
            "data": lista_carritos
        }

    except Exception as e:
        print(f"Error al obtener todos los carritos: {e}")
        return {
            "success": False,
            "message": "❌ Error al obtener los carritos"
        }


def obtener_carrito_usuario(user_cc: int):
    
    query = """
        SELECT 
            u.user_name,
            c.car_id,
            c.fecha_creacion,
            c.estado,
            p.product_name AS nombre_producto,
            cd.detalle_cantidad AS cantidad,
            p.product_price AS precio_unitario,
            (cd.detalle_cantidad * p.product_price) AS subtotal
        FROM carrito c
        INNER JOIN usuarios u ON u.user_cc = c.user_cc
        INNER JOIN carrito_detalle cd ON cd.car_id = c.car_id
        INNER JOIN productos p ON cd.product_id = p.product_id
        WHERE c.user_cc = %s AND c.estado = '1'
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
                "car_id": car_id,
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


def agregar_estado_carrito(car_id: int, data):
    try:
        query_check_carrito = """
            SELECT car_id
            FROM carrito
            WHERE car_id = %s
        """
        carrito = execute_query(query_check_carrito, (car_id,), fetchone=True)

        if not carrito:
            return {
                "success": False,
                "message": f"❌ Carrito con ID {car_id} no encontrado"
            }

        query_check_estado = """
            SELECT id 
            FROM carrito_estados 
            WHERE car_id = %s
            ORDER BY fecha_actualizacion DESC 
            LIMIT 1
        """
        estado_existente = execute_query(query_check_estado, (car_id,), fetchone=True)

        if estado_existente:
            query_update = """
                UPDATE carrito_estados
                SET estado = %s, comentario = %s, actualizado_por = %s, fecha_actualizacion = NOW()
                WHERE id = %s
            """
            params = (data.estado, data.comentario, data.actualizado_por, estado_existente[0])
            execute_query(query_update, params, commit=True)

            return {
                "success": True,
                "message": f"🔄 Estado del carrito {car_id} actualizado correctamente"
            }

        else:
            query_insert = """
                INSERT INTO carrito_estados (car_id, estado, comentario, actualizado_por, fecha_actualizacion)
                VALUES (%s, %s, %s, %s, NOW())
            """
            params = (car_id, data.estado, data.comentario, data.actualizado_por)
            execute_query(query_insert, params, commit=True)

            return {
                "success": True,
                "message": f"✅ Estado del carrito {car_id} agregado correctamente"
            }

    except Exception as e:
        print(f"❌ Error en agregar_estado_carrito: {e}")
        return {
            "success": False,
            "message": f"❌ Error al actualizar/insertar estado del carrito: {e}"
        }


def obtener_historial_carrito(car_id: int):
    try:
        query = """
            SELECT estado, comentario, fecha_actualizacion, actualizado_por 
            FROM carrito_estados
            WHERE car_id = %s
            ORDER BY fecha_actualizacion ASC
        """
        historial = execute_query(query, (car_id,), fetchall=True)

        if not historial:
            return {
                "success": True,
                "data": []  # Si no hay historial, devolvemos un arreglo vacío
            }

        lista_historial = []
        for row in historial:
            lista_historial.append({
                "estado": row[0],
                "comentario": row[1],
                "actualizado_por": row[2],
                "fecha": str(row[3])
            })

        return {
            "success": True,
            "data": lista_historial
        }

    except Exception as e:
        print(f"❌ Error al obtener historial del carrito {car_id}: {e}")
        return {
            "success": False,
            "message": f"Error al obtener historial: {e}"
        }


def eliminar_producto(detalle_id: int, car_id: int):
    
    try:
        query = """
            DELETE FROM carrito_detalle
            WHERE detalle_id = %s AND car_id = %s
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
    query_carrito = """
        SELECT car_id, estado
        FROM carrito
        WHERE car_id = %s AND estado = 1
    """
    carrito = execute_query(query_carrito, (car_id,), fetchone=True)

    if not carrito:
        return {"success": False, "message": f"❌ Carrito {car_id} no encontrado"}

    # carrito es una tupla: (car_id, estado)
    if carrito[1] == 0:
        return {"success": False, "message": "⚠️ Este carrito ya fue cerrado"}

    query_update = """
        UPDATE carrito
        SET estado = 0
        WHERE car_id = %s
    """
    execute_query(query_update, (car_id,))

    return {"success": True, "message": f"✅ Carrito {car_id} finalizado correctamente"}

