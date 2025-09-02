from fastapi import APIRouter
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from models.producto.product_class  import (create_product, all_categories, all_products, delete_product, update_product, view_product)

Product_router = APIRouter(
    prefix="/product",
    tags=["product"],
    include_in_schema=True
)


class ProductCreate(BaseModel):
    name: str
    description: str
    cant: int
    price: float
    category_id: int

class ProductUpdate(BaseModel):
    id: int
    name: str
    description: str
    category_id: int
    cant: int
    price: float



@Product_router.post("/create")
def create_product_route(data: ProductCreate):
    if create_product(data.name, data.description, data.cant, data.price, data.category_id):
        return JSONResponse(content={
            "success": True,
            "message": "Producto creado exitosamente"
        }, status_code=201)
    else:
        return JSONResponse(content={
            "success": False,
            "message": "Error al crear el producto"
        }, status_code=500)


@Product_router.get("/view/data")
def get_products():
    products = all_products()
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
    delete_product(id)
    return JSONResponse(content={"message": "Producto eliminado con éxito"})


@Product_router.get("/get_product/{id}")
def get_product(id: int):
    product = view_product(id)
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


@Product_router.put("/edit")
def edit_product(data: ProductUpdate):
    if update_product(data.id, data.name, data.description, data.category_id, data.cant, data.price):
        return JSONResponse(content={
            "success": True,
            "message": "Producto actualizado exitosamente"
        })
    else:
        return JSONResponse(content={
            "success": False,
            "message": "Error al actualizar producto"
        })


@Product_router.get("/all_categories")
def get_all_categories():
    categorias = all_categories()
    if not categorias:
        return JSONResponse({"message: " "no hay datos"}, 404)
    return JSONResponse(content=[{"id": c[0], "name": c[1]} for c in categorias])
