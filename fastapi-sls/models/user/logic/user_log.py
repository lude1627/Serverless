from fastapi import APIRouter
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from models.user.logic.user_consl import  register_user, update_user, view_user

user_router = APIRouter(
    prefix="/user",
    tags=["u"],
    include_in_schema=True
)

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



@user_router.post("/register")
def register(data: RegisterModel):
    if register_user(data.id, data.username, data.phone, data.email, data.password):
        return JSONResponse(content={
            "success": True,
            "message": "Usuario registrado exitosamente"
        })
    else:
        return JSONResponse(content={
            "success": False,
            "message": "Error al registrar usuario"
        })


@user_router.get("/view/{id}")
def get_user_json(id: int):
    user = view_user(id)
    if not user:
        return JSONResponse(content={"error": "Usuario no encontrado"}, status_code=404)
    return JSONResponse(content={
        "id": user[0],
        "username": user[1],
        "phone": user[2],
        "email": user[3],
        "password": user[4]
    })


@user_router.put("/update")
def updateP(data: UpdateUserModel):
    if update_user(data.id, data.username, data.phone, data.email, data.password):
        return JSONResponse(content={
            "success": True,
            "message": "Usuario actualizado exitosamente"
        })
    else:
        return JSONResponse(content={
            "success": False,
            "message": "Error al actualizar usuario"
        })
