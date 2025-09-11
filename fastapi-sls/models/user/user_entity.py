from pydantic import BaseModel

class RegisterModel(BaseModel):
    User_id: int
    username: str
    phone: int
    email: str
    password: str

class UpdateUserModel(BaseModel):
    User_id: int
    username: str
    phone: int
    email: str
    password: str