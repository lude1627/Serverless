from db import execute_query

def verificar_producto_existe(product_id: int):
    query = """
        SELECT Product_id, Product_name, Product_cant, Product_price
        FROM productos
        WHERE Product_id = %s
        LIMIT 1
    """
    producto = execute_query(query, (product_id,), fetchone=True)

    if not producto:
        return {
            "success": False,
            "message": f"❌ El producto con ID {product_id} no existe"
        }
        
    listar_product = {
        "Product_id": producto[0],
        "Product_name": producto[1],
        "Product_cant": producto[2],
        "Product_price": producto[3],
    }
    
    return {
        "success": True,
        "message": "✅ Producto encontrado",
        "producto": listar_product
    }

def verificar_cantidad(product_id: int, product_cant: int):
    """
    Verifica si el producto tiene suficiente cantidad disponible.
    """
    query = """
        SELECT Product_cant
        FROM productos
        WHERE Product_id = %s
        LIMIT 1
    """
    producto = execute_query(query, (product_id,), fetchone=True)

    if not producto:
        return {
            "success": False,
            "message": f"❌ El producto con ID {product_id} no existe"
        }

    stock = producto[0]

    if stock < product_cant:
        return {
            "success": False,
            "message": f"⚠️ Producto agotado o insuficiente. Stock disponible: {stock}, intentaste agregar {product_cant}"
        }

    return {
        "success": True,
        "message": f"✅ Stock suficiente: {product_cant} unidades reservadas",
        "stock_restante": stock - product_cant
    }
