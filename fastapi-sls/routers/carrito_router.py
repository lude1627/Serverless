from fastapi import APIRouter
from models.carrito.carrito_class import Carrito
from models.carrito.carrito_entity import CarritoEntity

carrito_router = APIRouter(
    prefix="/Carro", 
    tags=["Carrito"],
    include_in_schema=True
    )
carrito = Carrito()

@carrito_router.post("/agregar")
def agregarcar(carrito_data: CarritoEntity):
    return carrito.agregar_producto(carrito_data)

@carrito_router.put("/actualizar/{id}")
def actualizarcar(id: int, cantidad: int):
    return carrito.actualizar_cantidad(id, cantidad)

@carrito_router.delete("/eliminar/{id}")
def eliminarcar(id: int):
    return carrito.eliminar_producto(id)

@carrito_router.get("/usuario/{user_id}")
def obtenercar(user_id: int):
    return carrito.obtener_carrito_usuario(user_id)
