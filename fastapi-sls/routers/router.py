from models.login.logic.login_log import login_router
from models.user.logic.user_log import user_router
from models.categoria.logic.category_log import category_router
from models.producto.logic.product_log import Product_router
from models.carrito.logic.car_log import carrito_router

array_router = [
    login_router,
    user_router,
    category_router,
    Product_router,
    carrito_router
]