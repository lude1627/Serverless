from pydantic import BaseModel

class CarritoEntity(BaseModel):
    user_id: int
    product_id: int
    car_cantidad: int
    
class Updatecantidad(BaseModel):
    detalle_cantidad: int


class EliminarProducto(BaseModel):
    detalle_id: int
    car_id: int 
    
    
    
    
    

