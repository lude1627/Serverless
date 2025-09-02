from fastapi import APIRouter
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from models.login.logic.login_consl import Login
login_router = APIRouter(
    prefix="/login",
    tags=["login"],
    include_in_schema=True
)


class LoginModel(BaseModel):
    username: str
    password: str



@login_router.post("/sign_in")
def sign_in(data: LoginModel):
    user = Login.login_user(data.username, data.password)


    print(user)
    if user:
        user_id = user[0]
        return JSONResponse(content={
            "success": True,
            "message": f"Bienvenid@ {data.username}",
            "user_id": user_id
        })
    else:
        return JSONResponse(content={
            "success": False,
            "message": "Usuario o contraseña incorrectos"
        })


