from fastapi import APIRouter
from models.carrito.carrito_entity import CarritoEntity, EliminarProducto
from models.carrito.carrito_class import CarritoClass,Updatecantidad
from services.carrito_service import eliminar_producto, obtener_carrito_usuario


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


@carrito_router.delete("/eliminar")
def eliminar(carro: EliminarProducto):
    return eliminar_producto(carro.detalle_id, carro.car_id)


@carrito_router.put("/actualizar/{detalle_id}/{car_id}")
def actualizar(detalle_id: int,car_id:int, up:Updatecantidad):
    return carro.actualizar_producto(detalle_id,car_id,up)



