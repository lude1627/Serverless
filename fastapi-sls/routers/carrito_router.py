from fastapi import APIRouter
from models.carrito.carrito_entity import CarritoEntity, CarritoUpdate
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

@carrito_router.get("/usuario/{User_id}")
def obtener_carrito(User_id: int):
    return carro.obtener_carrito_usuario(User_id)

@carrito_router.delete("/eliminar/{Car_id}")
def eliminar(Car_id: int):
    return carro.eliminar_producto(Car_id)

@carrito_router.put("/actualizar/{Car_id}")
def actualizar(Car_id: int, data: CarritoUpdate):
    return carro.actualizar_cantidad(Car_id, data.Car_cantidad)

