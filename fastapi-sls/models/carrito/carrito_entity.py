from pydantic import BaseModel

class CarritoEntity(BaseModel):
    user_cc: int
    product_id: int
    car_cantidad: int
    
class Updatecantidad(BaseModel):
    detalle_cantidad: int
    
    
class EstadoUpdate(BaseModel):
    estado: int 
    comentario: str | None = None
    actualizado_por: str
    

class EliminarProducto(BaseModel):
    detalle_id: int
    car_id: int 
    
    
    
    
    

