from db import execute_query
from services.usuario_service import ValidateU
from datetime import datetime
from typing import Any, Dict

val = ValidateU()


from typing import Dict, Any

def verificar_carrito_activo(user_cc: int) -> Dict[str, Any]:
    try:
        # 1️⃣ Validar usuario
        usuario = val.verificar_usuario_existe(user_cc)
        if not usuario["existe"]:
            return {
                "success": False,
                "message": f"❌ No se puede crear carrito porque el usuario {user_cc} no existe"
            }

        # 2️⃣ Buscar carrito activo
        carrito = execute_query(
            """
            SELECT car_id
            FROM carrito
            WHERE user_cc = %s AND car_state = '1'
            LIMIT 1
            """,
            (user_cc,),
            fetchone=True
        )
        if carrito:
            return {
                "success": True,
                "message": "✅ Carrito activo encontrado",
                "car_id": carrito[0]  # <-- aquí ya es int
            }

        # 3️⃣ Obtener fase inicial
        fase_inicial = execute_query(
            "SELECT cf_fase, cf_name, cf_comment FROM carrito_fase ORDER BY cf_fase ASC LIMIT 1",
            fetchone=True
        )
        if not fase_inicial:
            return {"success": False, "message": "No hay fases definidas en cf"}

        cf_fase_ini, cf_name_ini, cf_comment_ini = fase_inicial

        # 4️⃣ Crear carrito y COMMIT inmediato
        execute_query(
            """
            INSERT INTO carrito (user_cc, cf_fase, car_creation_date, car_state)
            VALUES (%s, %s, NOW(), '1')
            """,
            (user_cc, cf_fase_ini),
            commit=True,
            return_id=True
        )

        # Recuperar último carrito creado para ese usuario
        carrito_row = execute_query(
            "SELECT car_id FROM carrito WHERE user_cc = %s ORDER BY car_id DESC LIMIT 1",
            (user_cc,),
            fetchone=True
        )
        if not carrito_row:
            return {"success": False, "message": "❌ No se pudo obtener el carrito recién creado"}

        car_id = carrito_row[0]

        # 5️⃣ Insertar en historial
        execute_query(
            """
            INSERT INTO carrito_historial
                (car_id, ch_update_date, ch_updated_by, cf_name, cf_comment)
            VALUES (%s, NOW(), %s, %s, %s)
            """,
            (car_id, "ADMIN", cf_name_ini, cf_comment_ini),
            commit=True
        )

        return {
            "success": True,
            "message": f"🛒 Carrito creado para el usuario {user_cc}",
            "car_id": car_id  # <-- ya como int
        }

    except Exception as e:
        return {
            "success": False,
            "message": f"❌ Error al verificar/crear carrito: {e}"
        }




def obtener_todos_carritos():
    query = """
        SELECT 
            c.car_id,
            c.cf_fase,
            u.user_cc, 
            u.user_name, 
            c.car_creation_date, 
            c.car_state, 
            cf.cf_name AS fase, 
            SUM(cd.cd_cant * p.product_price) AS total
        FROM carrito c
        INNER JOIN usuarios u ON c.user_cc = u.user_cc
        LEFT JOIN carrito_detalle cd ON c.car_id = cd.car_id
        LEFT JOIN productos p ON cd.product_id = p.product_id
        LEFT JOIN carrito_fase cf ON c.cf_fase = cf.cf_fase
        GROUP BY 
            c.car_id, u.user_cc, u.user_name, c.car_creation_date, c.car_state, cf.cf_name
        ORDER BY c.car_id ASC
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
                "cf_fase": row[1],
                "user_cc": row[2],
                "user_name": row[3],
                "car_creation_date": row[4].strftime("%Y-%m-%d"),
                "car_state": row[5],
                "fase": row[6],
                "total": f"${row[7]:,.0f}".replace(",", ".") if row[7] is not None else "$0"
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
            c.car_creation_date,
            c.car_state,
            SUM(cd.cd_cant * p.product_price) AS total
        FROM carrito c
        INNER JOIN usuarios u ON c.user_cc = u.user_cc
        LEFT JOIN carrito_detalle cd ON c.car_id = cd.car_id
        LEFT JOIN productos p ON cd.product_id = p.product_id
        WHERE u.user_cc = %s
        GROUP BY c.car_id, u.user_cc, u.user_name, c.car_creation_date, c.car_state
        ORDER BY c.car_creation_date DESC 
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
                "car_creation_date": row[3].strftime("%Y-%m-%d"),
                "car_state": row[4],
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
            c.car_creation_date,
            c.car_state,
            p.product_name AS nombre_producto,
            cd.cd_cant AS cantidad,
            p.product_price AS precio_unitario,
            (cd.cd_cant * p.product_price) AS subtotal
        FROM carrito c
        INNER JOIN usuarios u ON u.user_cc = c.user_cc
        INNER JOIN carrito_detalle cd ON cd.car_id = c.car_id
        INNER JOIN productos p ON cd.product_id = p.product_id
        WHERE c.user_cc = %s AND c.car_state = '1'
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
                "car_creation_date": str(fecha_creacion),
                "car_state": estado
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




# ======================== FUNCIONES PARA ADMIN =============================


def obtener_carrito_user_admin(car_id: int):
    
    query = """
        SELECT 
            u.user_name,
            c.car_id,
            c.car_creation_date,
            c.car_state,
            p.product_name AS nombre_producto,
            cd.cd_cant AS cantidad,
            p.product_price AS precio_unitario,
            (cd.cd_cant * p.product_price) AS subtotal
        FROM carrito c
        INNER JOIN usuarios u ON u.user_cc = c.user_cc
        INNER JOIN carrito_detalle cd ON cd.car_id = c.car_id
        INNER JOIN productos p ON cd.product_id = p.product_id
        WHERE c.car_id = %s
    """

    try:
        result = execute_query(query, (car_id,), fetchall=True)

        if not result:
            return {
                "success": False,
                "message": f"⚠️ El carrito {car_id} no tiene productos"
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
                "car_creation_date": str(fecha_creacion),
                "car_state": estado
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


def obtener_historial_carrito(car_id: int):
    try:
        query = """
            SELECT 
                ch.car_id, ch.cf_name AS estado, ch.cf_comment AS comentario, ch.ch_update_date AS fecha, ch.ch_updated_by AS actualizado_por
            FROM carrito_historial AS ch
            JOIN carrito AS c
            ON ch.car_id = c.car_id
            WHERE c.car_id = %s
            order by ch.ch_update_date ASC

        """
        historial = execute_query(query, (car_id,), fetchall=True)

        if not historial:
            return {
                "success": True,
                "data": [] 
            }

        lista_historial = []
        for row in historial:
            lista_historial.append({
                "estado": row[1],
                "comentario": row[2],
                "fecha": str(row[3]),           
                "actualizado_por": row[4]     
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
            WHERE cd_id = %s AND car_id = %s
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
        SELECT car_id, car_state
        FROM carrito
        WHERE car_id = %s AND car_state = 1
    """
    carrito = execute_query(query_carrito, (car_id,), fetchone=True)

    if not carrito:
        return {"success": False, "message": f"❌ Carrito {car_id} no encontrado"}

    
    if carrito[1] == 0:
        return {"success": False, "message": "⚠️ Este carrito ya fue cerrado"}
    

    query_2 = """
        UPDATE carrito
        SET car_state ='0', cf_fase = '1'
        WHERE car_id = %s
    """
    execute_query(query_2, (car_id,),commit=True)

    query_fase=" select cf_name, cf_comment from carrito_fase where cf_fase ='1'"
    fase = execute_query(query_fase, fetchone=True) 
    
    query_update = """
         INSERT INTO carrito_historial (car_id, cf_name, cf_comment, ch_update_date, ch_updated_by)
                VALUES (%s, %s, %s, NOW(), "ADMIN")
    """
    execute_query(query_update, (car_id, fase[0], fase[1]), commit=True)

   

    return {"success": True, "message": f"✅ Carrito {car_id} finalizado correctamente"}



def avanzar_estado_carrito(car_id: int, usuario: str = "ADMIN") -> Dict[str, Any]:
    try:
        # 1️⃣ Último estado del historial
        fila = execute_query(
            """
            SELECT cf_name
            FROM carrito_historial
            WHERE car_id = %s
            ORDER BY ch_update_date DESC
            LIMIT 1
            """,
            (car_id,),
            fetchone=True
        )

        if not fila:
            return {"success": False, "message": "Carrito sin historial"}

        estado_actual = fila[0]

        
        fases = execute_query(
            "SELECT cf_name, cf_comment FROM carrito_fase ORDER BY cf_fase ASC",
            fetchall=True
        )
        nombres_fases = [f[0] for f in fases]

        if estado_actual in ("Entregado", "Cancelado"):
            return {"success": False, "message": "Carrito ya finalizado"}

        idx = nombres_fases.index(estado_actual)

        if idx + 1 >= len(nombres_fases):
            return {"success": False, "message": "No hay fase siguiente"}

        nuevo_nombre, nuevo_comentario = fases[idx + 1]

        # 3️⃣ Insertar en historial con NOW() y usuario
        execute_query(
            """
            INSERT INTO carrito_historial
                (car_id, ch_update_date, ch_updated_by, cf_name, cf_comment)
            VALUES (%s, NOW(), %s, %s, %s)
            """,
            (car_id, usuario, nuevo_nombre, nuevo_comentario),
            commit=True
        )

        # 4️⃣ Actualizar la fase actual del carrito
        execute_query(
            "UPDATE carrito SET cf_fase = %s WHERE car_id = %s",
            (idx + 1, car_id),
            commit=True
        )

        return {
            "success": True,
            "message": f"Estado cambiado de {estado_actual} a {nuevo_nombre}"
        }

    except Exception as e:
        return {"success": False, "message": f"Error al avanzar estado: {e}"}

from datetime import datetime
from typing import Dict, Any

def cancelar_carrito(car_id: int, usuario: str = "admin"):
 
 
    try:
   
        fila = execute_query(
            """
            SELECT cf_name
            FROM carrito c
            JOIN carrito_fase f ON c.cf_fase = f.cf_fase
            WHERE c.car_id = %s
            """,
            (car_id,),
            fetchone=True
        )
        if not fila:
            return {"success": False, "message": "Carrito no encontrado"}

        if fila[0] == "Cancelado" or fila[0 =="Entregado"]:
            return {"success": False, "message": "El carrito ya ah sido cancelado o Entregado"}

        # 2️⃣ Obtener info de la fase 'Cancelado'
        cancel_info = execute_query(
            "SELECT cf_fase, cf_name, cf_comment FROM carrito_fase WHERE cf_name = 'Cancelado'",
            fetchone=True
        )
        if not cancel_info:
            return {"success": False, "message": "No existe fase 'Cancelado' en carrito_fase"}

        cf_fase_cancel, cf_name_cancel, cf_comment_cancel = cancel_info

        # 3️⃣ Actualizar carrito -> poner cf_fase de 'Cancelado'
        execute_query(
            "UPDATE carrito SET cf_fase = %s WHERE car_id = %s",
            (cf_fase_cancel, car_id),
            commit=True
        )

        # 4️⃣ Insertar en historial
        execute_query(
            """
            INSERT INTO carrito_historial
                (car_id, ch_update_date, ch_updated_by, cf_name, cf_comment)
            VALUES (%s, NOW(), %s, %s, %s)
            """,
            (car_id, usuario, cf_name_cancel, cf_comment_cancel),
            commit=True
        )

        return {"success": True, "message": "Carrito cancelado correctamente"}

    except Exception as e:
        return {"success": False, "message": f"Error al cancelar carrito: {e}"}
