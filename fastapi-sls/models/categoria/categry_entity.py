from pydantic import BaseModel  

class Category(BaseModel):
    name: str
    status: str
