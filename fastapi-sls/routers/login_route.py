from fastapi import APIRouter
from fastapi.responses import JSONResponse
from models.login.login_entity import LoginModel
from models.login.login_class import Login

login_router = APIRouter(
    prefix="/login",
    tags=["login"],
    include_in_schema=True
)

login=Login()




@login_router.post("/sign_in")
def login(data: LoginModel):
    user = login.login_user(data.username, data.password)


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


