from pydantic import BaseModel

class ProductCreate(BaseModel):
    name: str
    description: str
    cant: int
    price: float
    category_id: int

class ProductUpdate(BaseModel):
    id:int
    name: str
    description: str
    category_id: int
    cant: int
    price: float
