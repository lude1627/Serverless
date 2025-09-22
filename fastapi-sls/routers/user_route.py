from fastapi import APIRouter
from models.user.user_entity import RegisterModel, UpdateUserModel, AdminUpdateUserModel
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


@user_router.post("/admin/register")
def admin_register(data: AdminUpdateUserModel):
    return usuario.admin_register_user(data)


@user_router.get("/view/all")
def get_all_users():
    return usuario.view_all_users()


@user_router.get("/view/{user_id}")
def get_user_json(user_id: int):
    return usuario.view_user(user_id)


@user_router.put("/admin/update/{user_id}")
def admin_update_user(data: AdminUpdateUserModel):
    return usuario.admin_update_user(data)


@user_router.put("/update")
def update_user(data: UpdateUserModel):
    return usuario.update_user(data)