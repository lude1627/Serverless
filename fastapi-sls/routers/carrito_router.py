from fastapi import APIRouter
from models.carrito.carrito_entity import CarritoEntity
from models.carrito.carrito_class import CarritoClass

carrito_router = APIRouter(
    prefix="/carro", 
    tags=["Carrito"], 
    include_in_schema=True
)

carro = CarritoClass()

@carrito_router.post("/agregar")
def agregar(carrito: CarritoEntity):
    return carro.agregar_producto(carrito)

@carrito_router.get("/usuario/{user_id}")
def obtener_carrito(user_id: int):
    return carro.obtener_carrito_usuario(user_id)

@carrito_router.delete("/eliminar/{car_id}")
def eliminar(car_id: int):
    return carro.eliminar_producto(car_id)

@carrito_router.put("/actualizar/{car_id}")
def actualizar(car_id: int, cantidad: int):
    return carro.actualizar_cantidad(car_id, cantidad)
