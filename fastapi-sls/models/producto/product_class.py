from db import execute_query
from fastapi.responses import JSONResponse
from models.producto.product_entity import ProductCreate, ProductUpdate


class Productos:
            
    from fastapi.responses import JSONResponse

    def view_product(self, id: int):
        query = """
            SELECT product_id, product_name, product_description, product_cant, product_price, cat_id 
            FROM productos 
            WHERE product_id = %s AND product_status = '1'
        """
        try:
            product = execute_query(query, (id,), fetchone=True)
            if not product:
                return None
            
            return {   # 👈 devolvemos dict crudo
            "product_id": product[0],
            "product_name": product[1],
            "product_description": product[2],
            "product_cant": product[3],
            "product_price": float(product[4]),
            "category_id": product[5]
        }
        except Exception as e:
            print(f"Error al mostrar Producto: {e}")
            return JSONResponse(content={
                "success": False,
                "message": "Error interno al obtener el producto"
            }, status_code=500)



    def all_products(self):
      
        query = """
            SELECT p.Product_id, p.product_name, p.product_description,  
                   p.product_cant, p.Product_price, c.Cat_name 
            FROM productos p 
            INNER JOIN categorias c ON p.cat_id = c.cat_id and p.product_status = '1'
            ORDER BY p.product_name
        """
        try:
            products = execute_query(query, fetchall=True)

            if not products:
                return JSONResponse(content={
                        "success": True,
                        "message": "No hay productos registrados",
                        "data": []
                    },status_code=200)

            response = {
                "success": True,
                "message": "Productos obtenidos correctamente",
                "data": [
                    {
                        "id": p[0],
                        "nombre": p[1],
                        "descripcion": p[2],
                        "cantidad": p[3],
                        "precio": f"${p[4]:,.0f}",
                        "categoria": p[5]
                    } for p in products
                ]
            }
            return JSONResponse(content=response, status_code=200)

        except Exception as e:
            return JSONResponse(content={
                    "success": False,
                    "message": f"Error al obtener productos: {str(e)}",
                    "data": []
                },status_code=500)


    def update_product(self, data: ProductUpdate):
     
        if not data.id or data.id <= 0:
            return JSONResponse(content={"success": False, "message": "ID inválido"}, status_code=400)
        if not data.name or data.name.strip() == "":
            return JSONResponse(content={"success": False, "message": "El nombre es obligatorio"}, status_code=400)
        if data.cant < 0:
            return JSONResponse(content={"success": False, "message": "La cantidad no puede ser negativa"}, status_code=400)
        if data.price < 0:
            return JSONResponse(content={"success": False, "message": "El precio no puede ser negativo"}, status_code=400)

        query = """
            UPDATE productos  
            SET product_name = %s,  
                product_description = %s,  
                product_cant = %s,   
                Product_price = %s, 
                Cat_id = %s 
            WHERE Product_id = %s
        """
      
        try:
            rows = execute_query(query, (data.name, data.description, data.cant, data.price, data.category_id, data.id), commit=True)
            
            if rows == 0:
                return JSONResponse(content={"success": False, "message": "Producto no encontrado"}, status_code=404)

            return JSONResponse(content={
                "success": True,
                "message": "Producto actualizado exitosamente"
            })
        
        except Exception as e:
            print(f"Error al actualizar producto: {e}")
            return JSONResponse(content={
                "success": False,
                "message": "Error al actualizar producto"
            }, status_code=500)


    def delete_product(self, id: int):
        if not isinstance(id, int) or id <= 0:
            return JSONResponse(content={"success": False, "message": "ID inválido"}, status_code=400)

        query = "Update productos SET product_status = '0' WHERE Product_id = %s"

        try:
            rows = execute_query(query, (id,), commit=True)
            if rows == 0:
                return JSONResponse(content={"success": False, "message": "Producto no encontrado"}, status_code=404)

            return JSONResponse(content={"success": True, "message": "Producto eliminado con éxito"})
           
        except Exception as e:
            print(f"Error al eliminar el producto: {e}")
            return JSONResponse(content={"success": False, "message": "No se puede eliminar el producto"}, status_code=500)
        

    def all_categories(self):
        query = "SELECT cat_id, cat_name FROM categorias WHERE cat_status = '1'"
        try:
            categorias = execute_query(query, fetchall=True)
            if categorias:
                response = {
                    "success": True,
                    "message": "Categorías obtenidas exitosamente",
                    "data": {str(cat[0]): cat[1] for cat in categorias}
                }
                return JSONResponse(content=response, status_code=200)
            else:
                response = {
                    "success": True,
                    "message": "No hay categorías registradas",
                    "data": []
                }
                return JSONResponse(content=response, status_code=200)

        except Exception as e:
            response = {
                "success": False,
                "message": f"Error al obtener categorías: {str(e)}",
                "data": []
            }
            return JSONResponse(content=response, status_code=500)


    def create_product(self, data: ProductCreate):
    
        if not data.name or data.name.strip() == "":
            return JSONResponse(content={"success": False, "message": "El nombre es obligatorio"}, status_code=400)
        if data.cant < 0:
            return JSONResponse(content={"success": False, "message": "La cantidad no puede ser negativa"}, status_code=400)
        if data.price < 0:
            return JSONResponse(content={"success": False, "message": "El precio no puede ser negativo"}, status_code=400)
        if not data.category_id or data.category_id <= 0:
            return JSONResponse(content={"success": False, "message": "La categoría es obligatoria"}, status_code=400)

        query = """
            INSERT INTO productos (product_name, product_description, product_cant, product_price, cat_id, product_status) 
            VALUES (%s, %s, %s, %s, %s, '1')
        """
        try:
            execute_query(query, (data.name, data.description, data.cant, data.price, data.category_id), commit=True)
    
            return JSONResponse(content={
                    "success": True,
                    "message": "Producto creado exitosamente"
                }, status_code=201)

        except Exception as e:
            print(f"Error al crear un producto: {e}")
            return JSONResponse(content={
                    "success": False,
                    "message": "Error al crear el producto"
                }, status_code=500)
