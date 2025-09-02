from fastapi import APIRouter
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from models.categoria.logic.category_sonsl import create_cat, all_categories, delete_cat

category_router = APIRouter(
    prefix="/category",
    tags=["category"],
    include_in_schema=True)


class CategoryCreate(BaseModel):
    id: int
    name: str


@category_router.post("/create")
def create_category(data: CategoryCreate):
    if create_cat(data.id, data.name):
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
    categoria = all_categories()
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
    if delete_cat(id):
        return JSONResponse(content={
            "success": True,
            "message": "Categoría eliminada exitosamente"
        })
    else:
        return JSONResponse(content={
            "success": False,
            "message": "Error al eliminar categoría"
        }, status_code=500)
