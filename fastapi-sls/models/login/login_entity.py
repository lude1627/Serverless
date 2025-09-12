from pydantic import BaseModel

class LoginModel(BaseModel):
    user_cc: int
    password: str
   