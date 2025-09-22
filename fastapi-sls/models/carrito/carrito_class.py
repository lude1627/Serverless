from models.carrito.carrito_entity import CarritoEntity,Updatecantidad
from fastapi.responses import JSONResponse
from services.usuario_service import ValidateU
from services.producto_service import verificar_producto_existe, verificar_cantidad
from services.carrito_service import (
    verificar_carrito_activo,
    eliminar_producto
)
val = ValidateU()
from db import execute_query

class CarritoClass:
            
        def agregar_producto(self, carrito: CarritoEntity):
            
            try:
                resultado_usuario = val.verificar_usuario_existe(carrito.user_cc)
                if not resultado_usuario["success"]:
                    return resultado_usuario
                car_id = None
                
                # validar carrito
                resultado_carrito = verificar_carrito_activo(carrito.user_cc)
                if not resultado_carrito["success"]:
                    return resultado_carrito
                
                car_id = resultado_carrito["car_id"]
                
                # validar producto
                resultado_producto = verificar_producto_existe(carrito.product_id)
                if not resultado_producto["success"]:
                    return resultado_producto
                
          
                # validar cantidad
                resultado_cantidad = verificar_cantidad(carrito.product_id, carrito.car_cantidad)
                if not resultado_cantidad["success"]:
                    return resultado_cantidad
                
                
                # obtener precio del producto
                precio_unitario = resultado_producto["producto"]["product_price"]
                
                
                # insertar producto directamente aquí (antes estaba en el service)
                query = """
                    INSERT INTO carrito_detalle (car_id, product_id, detalle_cantidad, precio_unitario)
                    VALUES (%s, %s, %s, %s)
                """
                params = (car_id, carrito.product_id, carrito.car_cantidad, precio_unitario)
                execute_query(query, params, commit=True, return_id=True)

                
                return {
                    "success": True,
                    "message": f"✅ Producto {carrito.product_id} agregado al carrito {car_id}",
                    # "detalle": detalle
                }

                   
            except Exception as e:
                return {
                    "success": False,
                    "message": f"❌ Error al agregar producto: {e}"
                }
        
                
        def eliminar_producto(self, user_cc: int, detalle_id: int):
            try:
                resultado_usuario = val.verificar_usuario_existe(user_cc)
                if not resultado_usuario["success"]:
                    return resultado_usuario

                resultado_carrito = verificar_carrito_activo(user_cc)
                if not resultado_carrito["success"]:
                    return resultado_carrito

                resultado_eliminar = eliminar_producto(detalle_id, resultado_carrito["car_id"])
                if not resultado_eliminar["success"]:
                    return resultado_eliminar

               
                return {
                    "success": True,
                    "message": resultado_eliminar["message"],
                    # "carrito": carrito_actualizado
                }
            except Exception as e:
                return {
                    "success": False,
                    "message": f"Error al eliminar producto: {e}"
                }

        def actualizar_producto(self, detalle_id: int,car_id:int,up:Updatecantidad):
            query = """
                UPDATE carrito_detalle
                SET detalle_cantidad = %s
                WHERE detalle_id = %s and car_id = %s
            """
            try:
                rows = execute_query(query, (up.detalle_cantidad,detalle_id,car_id ), commit=True)

                if rows == 0:
                    return JSONResponse(
                        content={"success": False, "message": "Carrito no encontrado"},
                        status_code=404
                    )
    
                return JSONResponse(
                    content={"success": True, "message": "Carrito actualizado exitosamente"}
                )

            except Exception as e:
                return {
                    "success": False,
                    "message": f"❌ Error al actualizar producto: {e}"
                }


        def ver_detalles_por_carrito(self, car_id: int):
            query = """
                SELECT d.detalle_id,
                    d.car_id,
                    d.product_id,
                    d.detalle_cantidad,
                    d.precio_unitario,
                    p.product_name AS nombre_producto   
                FROM carrito_detalle d
                JOIN productos p ON p.product_id = d.product_id
                WHERE d.car_id = %s
            """
            try:
                filas = execute_query(query, (car_id,), fetchall=True)
                if not filas:
                    return {"success": False, "detalles": []}

                detalles = []
                for r in filas:
                    detalles.append({
                        "detalle_id": r[0],
                        "car_id": r[1],
                        "product_id": r[2],
                        "detalle_cantidad": r[3],
                        "precio_unitario": float(r[4]),
                        "nombre_producto": r[5]          
                    })
                return {"success": True, "detalles": detalles}
            except Exception as e:
                return {"success": False, "message": f"❌ Error: {e}"}

        
        
        
        
        
        
        
        
        


        


        

            



