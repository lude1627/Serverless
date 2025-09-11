from models.carrito.carrito_entity import CarritoEntity
from services.usuario_service import verificar_usuario_existe
from services.producto_service import verificar_producto_existe, verificar_cantidad
from services.carrito_service import (
    verificar_carrito_activo, 
    obtener_carrito_usuario,
    # insertar_producto,
    eliminar_producto,
    actualizar_cantidad
)

from db import execute_query

class CarritoClass:
            
        def agregar_producto(self, carrito: CarritoEntity):
            
            try:
                car_id = None
                
                print("llego1")
                #validar carrito
                #validar carrito 
                resultado_carrito = verificar_carrito_activo(carrito.user_id)
                if not resultado_carrito["success"]:
                    return resultado_carrito
                
                car_id = resultado_carrito["car_id"]
                
                print("llego2")
                #validar producto
                resultado_producto = verificar_producto_existe(carrito.product_id)
                if not resultado_producto["success"]:
                    return resultado_producto
                
                print("llego3")
                #validar cantidad
                resultado_cantidad = verificar_cantidad(carrito.product_id, carrito.car_cantidad)
                if not resultado_cantidad["success"]:
                    return resultado_cantidad
                
                print("llego4")
                # obtener precio del producto
                precio_unitario = resultado_producto["producto"]["Product_price"]
                
                print("llego4.5")
                
                # 5️⃣ insertar producto directamente aquí (antes estaba en el service)
                query = """
                    INSERT INTO carrito_detalle (Car_id, Product_id, Detalle_cantidad, precio_unitario)
                    VALUES (%s, %s, %s, %s)
                """
                params = (car_id, carrito.product_id, carrito.car_cantidad, precio_unitario)
                detalle = execute_query(query, params, commit=True, return_id=True)
                print("llego4.6")
                
              
                
                
                print("llego5")
                return {
                    "success": True,
                    "message": f"✅ Producto {carrito.product_id} agregado al carrito {car_id}",
                    "detalle": detalle
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


        def actualizar_producto(self, user_id: int, product_id: int, nueva_cantidad: int):
            try:

                resultado_usuario = verificar_usuario_existe(user_id)
                if not resultado_usuario["existe"]:
                    return resultado_usuario

                resultado_carrito = verificar_carrito_activo(user_id)
                if not resultado_carrito["success"]:
                    return resultado_carrito

                car_id = resultado_carrito["car_id"]

                resultado_producto = verificar_producto_existe(product_id)
                if not resultado_producto["success"]:
                    return resultado_producto

                stock = resultado_producto["producto"]["Product_stock"]
                if nueva_cantidad > stock:
                    return {
                        "success": False,
                        "message": f"⚠️ Stock insuficiente. Disponible: {stock}, solicitado: {nueva_cantidad}"
                    }

                resultado_actualizar = actualizar_cantidad(car_id, product_id, nueva_cantidad)
                if not resultado_actualizar["success"]:
                    return resultado_actualizar

                carrito_actualizado = obtener_carrito_usuario(user_id)

                return {
                    "success": True,
                    "message": f"♻️ Cantidad actualizada para producto {product_id}",
                    "carrito": carrito_actualizado
                }

            except Exception as e:
                return {
                    "success": False,
                    "message": f"❌ Error al actualizar producto: {e}"
                }


        
        
        
        
        
        
        
        
        
        


        


        

            



