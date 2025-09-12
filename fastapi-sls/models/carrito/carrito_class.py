from models.carrito.carrito_entity import CarritoEntity,Updatecantidad
from fastapi.responses import JSONResponse
from services.usuario_service import verificar_usuario_existe
from services.producto_service import verificar_producto_existe, verificar_cantidad
from services.carrito_service import (
    verificar_carrito_activo,
    eliminar_producto
)

from db import execute_query

class CarritoClass:
            
        def agregar_producto(self, carrito: CarritoEntity):
            
            try:
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
                precio_unitario = resultado_producto["producto"]["Product_price"]
                
                
                # insertar producto directamente aquí (antes estaba en el service)
                query = """
                    INSERT INTO carrito_detalle (Car_id, Product_id, Detalle_cantidad, precio_unitario)
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
                resultado_usuario = verificar_usuario_existe(user_cc)
                if not resultado_usuario["success"]:
                    return resultado_usuario

                resultado_carrito = verificar_carrito_activo(user_cc)
                if not resultado_carrito["success"]:
                    return resultado_carrito

                resultado_eliminar = eliminar_producto(detalle_id, resultado_carrito["car_id"])
                if not resultado_eliminar["success"]:
                    return resultado_eliminar

                # carrito_actualizado = obtener_carrito_usuario(user_id)
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
                SET Detalle_cantidad = %s
                WHERE Detalle_id = %s and Car_id = %s
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



        
        
        
        
        
        
        
        
        
        


        


        

            



