from pydantic import BaseModel

class RegisterModel(BaseModel):
    id: int
    username: str
    phone: int
    email: str
    password: str

class UpdateUserModel(BaseModel):
    id: int
    username: str
    phone: int
    email: str
    password: str