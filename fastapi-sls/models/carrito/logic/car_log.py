from fastapi import APIRouter
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from models.carrito.logic.car_consl import view_cart

carrito_router = APIRouter(
    prefix="/carrito",
    tags=["carrito"],
    include_in_schema=True
)


class AddCartModel(BaseModel):
    user_id: int
    product_id: int

 
class ViewCartModel(BaseModel):
    user_id: int



@carrito_router.get("/view/{user_id}")
def view_cart(user_id: int):
    items = view_cart(user_id)
    if items:
        return JSONResponse(content={"success": True, "items": items})
    return JSONResponse(content={"success": False, "message": "No hay productos en el carrito"})
