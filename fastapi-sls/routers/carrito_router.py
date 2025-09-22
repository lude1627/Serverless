from fastapi import APIRouter
from models.carrito.carrito_entity import CarritoEntity, EstadoUpdate
from models.carrito.carrito_class import CarritoClass,Updatecantidad
from services.carrito_service import (
    eliminar_producto, 
    obtener_carrito_usuario, 
    finalizar_compra, 
    obtener_todos_carritos,
    agregar_estado_carrito,
    obtener_historial_carrito
)



carrito_router = APIRouter(
    prefix="/carro", 
    tags=["Carrito"], 
    include_in_schema=True
)

carro = CarritoClass()

@carrito_router.post("/agregar")
def agregar(carrito: CarritoEntity):
    return carro.agregar_producto(carrito)


@carrito_router.get("/view/all")
def listar_carritos():
    return obtener_todos_carritos()


@carrito_router.get("/usuario/{user_cc}")
def obtener_carrito(user_cc: int):
    return obtener_carrito_usuario(user_cc)


@carrito_router.delete("/eliminar/{detalle_id}/{car_id}")
def eliminar(detalle_id: int, car_id: int):
    return eliminar_producto(detalle_id, car_id)

@carrito_router.get("/dcarrito/{car_id}")
def obtener_detalles_carrito(car_id: int):
    return carro.ver_detalles_por_carrito(car_id)

@carrito_router.get("/{car_id}/historial")
def historial_carrito(car_id: int):
    return obtener_historial_carrito(car_id)


@carrito_router.put("/{car_id}/estado")
def agregar_estado(car_id: int, data: EstadoUpdate):
    return agregar_estado_carrito(car_id, data)


@carrito_router.put("/actualizar/{detalle_id}/{car_id}")
def actualizar(detalle_id: int,car_id:int, up:Updatecantidad):
    return carro.actualizar_producto(detalle_id,car_id,up)

@carrito_router.put("/finalizar/{car_id}")
def finalizar(car_id: int):
    return finalizar_compra(car_id)



 