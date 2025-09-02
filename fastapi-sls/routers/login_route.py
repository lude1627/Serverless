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
def log(data: LoginModel):
 
    return Login.login_user(data.username, data.password)

