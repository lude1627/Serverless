from fastapi import APIRouter
from fastapi.responses import JSONResponse
from models.categoria.categry_entity import CategoryCreate
from models.categoria.category_class import Categoria

category_router = APIRouter(
    prefix="/category",
    tags=["category"],
    include_in_schema=True)

categorias = Categoria()


@category_router.post("/create")
def create_category(data: CategoryCreate):
    if categorias.create_cat(data.id, data.name):
        return JSONResponse(content={
            "success": True,
            "message": "Categoría creada exitosamente"
        }, status_code=201)
    else:
        return JSONResponse(content={
            "success": False,
            "message": "Error al crear categoría"
        }, status_code=500)


@category_router.get("/view/data")
def get_category():
    categoria = categorias.all_categories()
    if not categoria:  
        return JSONResponse(content=[])
    category_json = [
        {
            "Cat_id": cat[0],
            "Cat_name": cat[1]
        }
        for cat in categoria
    ]
    return JSONResponse(content=category_json)


@category_router.delete("/delete/{id}")
def delete_category(id: int):
    if categorias.delete_cat(id):
        return JSONResponse(content={
            "success": True,
            "message": "Categoría eliminada exitosamente"
        })
    else:
        return JSONResponse(content={
            "success": False,
            "message": "Error al eliminar categoría"
        }, status_code=500)
