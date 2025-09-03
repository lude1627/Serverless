from fastapi import APIRouter
from fastapi.responses import JSONResponse
from models.carrito.car_class import Carrito

carrito_router = APIRouter(
    prefix="/carrito",
    tags=["carrito"],
    include_in_schema=True
)

carrito = Carrito()


@carrito_router.get("/view/{user_id}")
def view_cart(user_id: int):
    items = view_cart(user_id)
    if items:
        return JSONResponse(content={"success": True, "items": items})
    return JSONResponse(content={"success": False, "message": "No hay productos en el carrito"})
