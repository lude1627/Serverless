from pydantic import BaseModel

class CarritoEntity(BaseModel):
    user_id: int
    product_id: int
    
    car_cantidad: int
    
    
class ActualizarCarrito(BaseModel):
    detalle_id: int
    nueva_cantidad: int
    
    
class EliminarProducto(BaseModel):
    detalle_id: int
    car_id: int 
    
    
class Ver_carrito(BaseModel):
    user_id: int
    
