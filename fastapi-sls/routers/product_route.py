from fastapi import APIRouter
from fastapi.responses import JSONResponse
from models.producto.product_entity import ProductCreate, ProductUpdate
from models.producto.product_class  import Productos

Product_router = APIRouter(
    prefix="/product",
    tags=["product"],
    include_in_schema=True
)

productos = Productos()


@Product_router.post("/create")
def create_product_route(data: ProductCreate):
    return productos.create_product(data)
       
@Product_router.get("/view/data")
def get_products():
    return  productos.all_products()  


@Product_router.put("/delete/{id}")
def deleteP(id: int):
    return productos.delete_product(id)


@Product_router.get("/get_product/{id}")
def get_product(id: int):
    product = productos.view_product(id)
    if not product:
        return JSONResponse(
            content={"success": False, "message": "Producto no encontrado"},
            status_code=404
        )
        
    return JSONResponse(content=product, status_code=200)
    

@Product_router.put("/edit/{id}")
def edit_product( data: ProductUpdate):
    return productos.update_product(data)
       


@Product_router.get("/all_categories")
def get_all_categories():
    return productos.all_categories()

