from pydantic import BaseModel

class CarritoEntity(BaseModel):
    user_id: int
    product_id: int
    Car_cantidad: int
    
class CarritoUpdate(BaseModel):
    Car_cantidad: int
    
