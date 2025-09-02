from pydantic import BaseModel  

class CategoryCreate(BaseModel):
    id: int
    name: str
