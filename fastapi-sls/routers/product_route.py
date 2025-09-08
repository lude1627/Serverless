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
    products = productos.all_products()
    productos_json = [
        {
            "id": p[0],
            "nombre": p[1],
            "descripcion": p[2],
            "cantidad": p[3],
            "precio": p[4],
            "categoria": p[5]
        }
        for p in products
    ]
    return JSONResponse(content=productos_json)


@Product_router.delete("/delete/{id}")
def deleteP(id: int):
    return productos.delete_product(id)


@Product_router.get("/get_product/{id}")
def get_product(id: int):
    product = productos.view_product(id)
    if not product:
        return JSONResponse(content={"error": "Producto no encontrado"}, status_code=404)
    return JSONResponse(content={
        "id": product[0],
        "name": product[1],
        "description": product[2],
        "cant": product[3],
        "price": product[4],
        "category_id": product[5]
    })


@Product_router.put("/edit/{id}")
def edit_product( data: ProductUpdate):
    return productos.update_product(data)
       


@Product_router.get("/all_categories")
def get_all_categories():
    categorias = productos.all_categories()
    if not categorias:
        return JSONResponse({"message: " "no hay datos"}, 404)
    return JSONResponse(content= categorias)
