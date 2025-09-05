from pydantic import BaseModel

class CarritoEntity(BaseModel):
    user_id: int
    product_id: int
    car_cantidad: int
    
    
class ActualizarCarrito(BaseModel):
    nueva_cantidad: int
    
