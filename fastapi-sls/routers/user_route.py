from fastapi import APIRouter
from fastapi.responses import JSONResponse
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
    if usuario.register_user(data.id, data.username, data.phone, data.email, data.password):
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
    user =usuario.view_user(id)
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
    if usuario.update_user(data.id, data.username, data.phone, data.email, data.password):
        return JSONResponse(content={
            "success": True,
            "message": "Usuario actualizado exitosamente"
        })
    else:
        return JSONResponse(content={
            "success": False,
            "message": "Error al actualizar usuario"
        })
