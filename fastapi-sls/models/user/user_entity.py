from pydantic import BaseModel

class RegisterModel(BaseModel):
    user_cc: int
    username: str
    phone: int
    email: str
    password: str

class UpdateUserModel(BaseModel):
    user_cc: int
    username: str
    phone: int
    email: str
    password: str