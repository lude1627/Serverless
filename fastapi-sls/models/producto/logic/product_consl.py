from db import execute_query

def add_to_cart(product_id: int, user_id: int, cantidad: int):
    query = """
        INSERT INTO carrito (User_id, Product_id, Car_Cantidad)
        VALUES (%s, %s, %s)
        ON DUPLICATE KEY UPDATE Car_Cantidad = Car_Cantidad + VALUES(Car_Cantidad);
    """
    try:

     carrito = execute_query(query, (user_id, product_id, cantidad), fetchall=True)
   
     return carrito
    except Exception as e:
         print("Error al guardar las compras: {e}")
         return False 
         
def view_product(id: int):
    query = " SELECT Product_id, Product_name, Product_description,  Product_cant, Product_price, Cat_id FROM productos WHERE Product_id = %s "
    try:
        product = execute_query(query,(id),fechnone=True)
        return product
    except Exception as e:
        print(f"Error al mostrar Producto: {e}")



def all_products():
    
    query = """ SELECT p.Product_id, p.Product_name, p.Product_description,  p.Product_cant, p.Product_price, c.Cat_name FROM productos p INNER JOIN categorias c ON p.Cat_id = c.Cat_id ORDER BY p.Product_name
    """
    try: 
        products = execute_query(query,fetchall=True)
        return products
    except Exception as e:
        print(f"Error al mostrar productos: {e}") 
        return []   


def update_product(id: int, name: str, description: str, cant: int, price: float, cat_id: int) -> bool:
    query = " UPDATE productos  SET Product_name = %s,  Product_description = %s,  Product_cant = %s,   Product_price = %s, Cat_id = %s WHERE Product_id = %s "
    try:
        execute_query(query,(id,name,description,cant,price,cat_id),commit=True)
        return True
    except Exception as e:
        print("Error al actualizar producto: {e}")
        return False



def delete_product(id: int):
   
    query = "DELETE FROM productos WHERE Product_id = %s"

    try:
        execute_query(query,(id),commit=True)
        return True
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




def create_product(name, description, cant, price, category_id):
    query = " INSERT INTO productos (Product_name, Product_description, Product_cant, Product_price, Cat_id) VALUES (%s, %s, %s, %s, %s)"
    try:
        execute_query(query, (name, description, cant, price, category_id), commit=True)
        return True
    except Exception as e:
        print("Error al crear un producto: {e}")
        return False