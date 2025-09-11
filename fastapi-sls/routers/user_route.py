from fastapi import APIRouter
from models.user.user_entity import RegisterModel, UpdateUserModel
from models.user.user_class import Usuario

user_router = APIRouter(
    prefix="/user",
    tags=["usuario"],
    include_in_schema=True
)

usuario = Usuario()


@user_router.post("/register")
def register(data: RegisterModel):
        return usuario.register_user(data)


@user_router.get("/view/{User_id}")
def get_user_json(User_id: int):
    return usuario.view_user(User_id)


@user_router.put("/update")
def updateP(data: UpdateUserModel):
   return usuario.update_user(data)
