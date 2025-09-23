from pydantic import BaseModel
from typing import Optional


class RegisterModel(BaseModel):
    user_cc: int
    username: str
    phone: int
    email: str
    password: str


class UpdateUserModel(BaseModel):
    user_id: int
    user_cc: int
    username: str
    phone: int
    email: str
   

class AdminUpdateUserModel(BaseModel):
    user_id: Optional[int] = None
    user_cc: int
    username: str
    phone: int
    email: str
    user_type: int  
    user_status: int  
    password: Optional[str] = None 