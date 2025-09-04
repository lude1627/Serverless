from .login_route import login_router
from .user_route import user_router
from .category_route import category_router
from .product_route import Product_router
from .carrito_router import carrito_router


array_router = [
    login_router,
    user_router,
    category_router,
    Product_router,
    carrito_router
]