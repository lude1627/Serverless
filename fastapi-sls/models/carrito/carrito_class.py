from models.carrito.carrito_entity import CarritoEntity, ActualizarCarrito
from services.usuario_service import verificar_usuario_existe
from services.carrito_service import verificar_carrito_activo, obtener_carrito_usuario
from services.producto_service import verificar_producto_existe, verificar_cantidad

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
                
                #insertar producto al carrito
                query = """
                INSERT INTO carrito_detalle (Car_id, Product_id, Product_cant)
                VALUES (%s, %s, %s, %s)
                """
                precio_unitario = resultado_producto["producto"]["Product_price"]
                params = (resultado_carrito["car_id"], carrito.product_id, carrito.car_cantidad, precio_unitario)
                
                execute_query(query, params, commit=True)
                
                #obtener carrito actualizado
                carrito_actualizado = obtener_carrito_usuario(carrito.user_id)
                
                return {
                    "success": True,
                    "message": f"✅ Producto {carrito.product_id} agregado al carrito {resultado_carrito['car_id']}",
                    "carrito": carrito_actualizado
                }
                
            except Exception as e:
                return {
                    "success": False,
                    "message": f"❌ Error al agregar producto: {e}"
                }

        
        
        
        
        
        
        
        
        
        


        


        

            



