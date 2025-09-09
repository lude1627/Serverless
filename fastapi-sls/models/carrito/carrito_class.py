from models.carrito.carrito_entity import CarritoEntity
from services.usuario_service import verificar_usuario_existe
from services.producto_service import verificar_producto_existe, verificar_cantidad
from services.carrito_service import (
    verificar_carrito_activo, 
    obtener_carrito_usuario,
    insertar_producto,
    eliminar_producto,
    actualizar_cantidad
)

from db import execute_query

class CarritoClass:
            
        def agregar_producto(self, carrito: CarritoEntity):
            
            try:
                #validar usuario
                resultado_usuario = verificar_usuario_existe(carrito.user_id)
                if not resultado_usuario["success"]:
                    return resultado_usuario
                
                #validar carrito
                resultado_carrito = verificar_carrito_activo(carrito.user_id)
                if not resultado_carrito["success"]:
                    return resultado_carrito
               
                #validar producto
                resultado_producto = verificar_producto_existe(carrito.product_id)
                if not resultado_producto["success"]:
                    return resultado_producto
               
                #validar cantidad
                resultado_cantidad = verificar_cantidad(carrito.product_id, carrito.car_cantidad)
                if not resultado_cantidad["success"]:
                    return resultado_cantidad
                
                # obtener precio del producto
                precio_unitario = resultado_producto["producto"]["Product_price"]

                # insertar producto al carrito
                insertar_producto(
                    resultado_carrito["car_id"], 
                    carrito.product_id, 
                    carrito.car_cantidad, 
                    precio_unitario
                )
                
                #obtener carrito actualizado
                carrito_actualizado = obtener_carrito_usuario(carrito.user_id)
                
                return {
                    "success": True,
                    "message": f"✅ Producto {carrito.product_id} agregado al carrito",
                    # "carrito": carrito_actualizado
                }
                    
            except Exception as e:
                return {
                    "success": False,
                    "message": f"❌ Error al agregar producto: {e}"
                }
                
        def eliminar_producto(self, user_id: int, detalle_id: int):
            try:
                resultado_usuario = verificar_usuario_existe(user_id)
                if not resultado_usuario["success"]:
                    return resultado_usuario

                resultado_carrito = verificar_carrito_activo(user_id)
                if not resultado_carrito["success"]:
                    return resultado_carrito

                resultado_eliminar = eliminar_producto(detalle_id, resultado_carrito["car_id"])
                if not resultado_eliminar["success"]:
                    return resultado_eliminar

                carrito_actualizado = obtener_carrito_usuario(user_id)
                return {
                    "success": True,
                    "message": resultado_eliminar["message"],
                    "carrito": carrito_actualizado
                }
            except Exception as e:
                return {
                    "success": False,
                    "message": f"Error al eliminar producto: {e}"
                }

                
        def actualizar_cantidad_producto(self, user_id: int, detalle_id: int, nueva_cantidad: int):
            try:
                resultado_usuario = verificar_usuario_existe(user_id)
                if not resultado_usuario["success"]:
                    return resultado_usuario

                resultado_carrito = verificar_carrito_activo(user_id)
                if not resultado_carrito["success"]:
                    return resultado_carrito

                # obtener product_id del detalle
                query_check = """
                    SELECT Product_id 
                    FROM carrito_detalle
                    WHERE Detalle_id = %s AND Car_id = %s
                    LIMIT 1
                """
                detalle = execute_query(query_check, (detalle_id, resultado_carrito["car_id"]), fetchone=True)

                if not detalle:
                    return {"success": False, "message": "❌ El producto no fue encontrado en el carrito"}

                product_id = detalle[0]

                resultado_update = actualizar_cantidad(detalle_id, resultado_carrito["car_id"], nueva_cantidad, product_id)
                if not resultado_update["success"]:
                    return resultado_update

                carrito_actualizado = obtener_carrito_usuario(user_id)
                return {
                    "success": True,
                    "message": resultado_update["message"],
                    "carrito": carrito_actualizado
                }

            except Exception as e:
                return {"success": False, "message": f"❌ Error al actualizar cantidad: {e}"}

        
        
        
        
        
        
        
        
        
        


        


        

            



