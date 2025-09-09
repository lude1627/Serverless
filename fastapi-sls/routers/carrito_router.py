from fastapi import APIRouter
from models.carrito.carrito_entity import CarritoEntity
from models.carrito.carrito_class import CarritoClass
from services.carrito_service import eliminar_producto, actualizar_cantidad, obtener_carrito_usuario

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
    return obtener_carrito_usuario(user_id)

@carrito_router.delete("/eliminar/{detalle_id}")
def eliminar(detalle_id: int):
    return eliminar_producto(detalle_id)

@carrito_router.put("/actualizar/{detalle_id}/{nueva_cantidad}")
def actualizar(detalle_id: int, nueva_cantidad: int):
    return actualizar_cantidad(detalle_id, nueva_cantidad)



