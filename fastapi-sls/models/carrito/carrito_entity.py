from pydantic import BaseModel

class CarritoEntity(BaseModel):
    user_id: int
    product_id: int
    cantidad: int
