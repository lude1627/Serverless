from fastapi import APIRouter
from models.categoria.categry_entity import Category
from models.categoria.category_class import Categoria

category_router = APIRouter(
    prefix="/category",
    tags=["category"],
    include_in_schema=True
)

categorias = Categoria()


@category_router.post("/create")
def create_category(data: Category):
    return categorias.create_cat(data.name)


@category_router.get("/view/data")
def get_category():
    categoria = categorias.all_categories()
    return categoria

@category_router.put("/update/{id}")
def update_category(id: int, data: Category):
    return categorias.update_cat(id, data.name, data.status)


@category_router.put("/delete/{id}")
def delete_category(id: int):
    return categorias.delete_cat(id)
    
    
    
    
