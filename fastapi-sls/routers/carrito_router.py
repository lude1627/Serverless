from fastapi import APIRouter
from models.carrito.carrito_entity import CarritoEntity, ActualizarCarrito
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

@carrito_router.delete("/eliminar/{detalle_id}")
def eliminar(detalle_id: int):
    return carro.eliminar_producto(detalle_id)

@carrito_router.put("/actualizar/{detalle_id}")
def actualizar(detalle_id: int, request: ActualizarCarrito):
    return carro.actualizar_cantidad_producto(detalle_id, request.nueva_cantidad)



