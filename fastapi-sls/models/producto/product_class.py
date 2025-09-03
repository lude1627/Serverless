from db import execute_query
from fastapi.responses import JSONResponse
from models.producto.product_entity import ProductCreate, ProductUpdate

class Productos:
            
    def view_product(self, id: int):
        query = " SELECT Product_id, Product_name, Product_description,  Product_cant, Product_price, Cat_id FROM productos WHERE Product_id = %s "
        try:
            product = execute_query(query,(id),fechnone=True)
            return product
        except Exception as e:
            print(f"Error al mostrar Producto: {e}")



    def all_products(self):
        
        query = """ SELECT p.Product_id, p.Product_name, p.Product_description,  p.Product_cant, p.Product_price, c.Cat_name FROM productos p INNER JOIN categorias c ON p.Cat_id = c.Cat_id ORDER BY p.Product_name
        """
        try: 
            products = execute_query(query,fetchall=True)
            return products
        except Exception as e:
            print(f"Error al mostrar productos: {e}") 
            return []   


    def update_product(self,data: ProductUpdate):

        description = data.description
        name = data.name
        cant = data.cant
        price = data.price
        category_id = data.category_id
        query = " UPDATE productos  SET Product_name = %s,  Product_description = %s,  Product_cant = %s,   Product_price = %s, Cat_id = %s WHERE Product_id = %s "
        try:
            update = execute_query(query,(id,name,description,cant,price,category_id),commit=True)
            if update:
                return JSONResponse(content={
                "success": True,
                "message": "Producto actualizado exitosamente"
                })
            else:
                return JSONResponse(content={
                    "success": False,
                    "message": "Error al actualizar producto"
                })
        except Exception as e:
                print("Error al actualizar producto: {e}")
                return False



    def delete_product(self, id: int):
    
        query = "DELETE FROM productos WHERE Product_id = %s"

        try:
            borrar = execute_query(query,(id),commit=True)
            if borrar:
                return JSONResponse(content={"message": "Producto eliminado con éxito"})
            else:
                return JSONResponse(content={"message": "No se puede eliminar el producto"})
        except Exception as e:
            print("Error al eliminar el producto: {e}")
            return 
        

    
    def get_category():
    
        query = "SELECT * FROM categorias"
        try:
            execute_query(query,(id),commit=True)
            return True
        except Exception as e:
            print("Error al traer las categorias: {e}")
            return False



    def all_categories():
    
        query="SELECT Cat_id, Cat_name FROM categorias"
        try:
            categorias = execute_query(query,fetchall=True)  
            return categorias
        except Exception as e:

            print("Error al mostrar las categorias : {e}")




    def create_product(self, data: ProductCreate):

        description = data.description
        name = data.name
        cant = data.cant
        price = data.price
        category_id = data.category_id

        query = " INSERT INTO productos (Product_name, Product_description, Product_cant, Product_price, Cat_id) VALUES (%s, %s, %s, %s, %s)"
        try:
            execute_query(query, (name, description, cant, price, category_id), commit=True) 
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