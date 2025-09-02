from db import execute_query

def view_cart(user_id: int):
    query = """
        SELECT 
            u.User_id,
            u.User_name,
            p.Product_id,
            p.Product_name,
            p.Product_description,
            p.Product_price,
            1 AS Car_cant,
            (p.Product_price * 1) AS Car_total
        FROM usuarios u
        INNER JOIN carrito c ON u.User_id = c.User_id
        INNER JOIN productos p ON c.Product_id = p.Product_id
        WHERE u.User_id = %s
    """
    try:
        return execute_query(query, (user_id,), fetchall=True)
    except Exception as e:
        print(f"Error en get_carrito: {e}")
        return None
