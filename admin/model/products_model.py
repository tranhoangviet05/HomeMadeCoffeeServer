from db import get_db_connection, release_db_connection
from psycopg2.extras import DictCursor

def get_products(category_id: int):
    conn = None

    try:
        conn = get_db_connection()
        cursor = conn.cursor(cursor_factory=DictCursor)

        cursor.execute("""
            SELECT product_id, product_name, description, price, image_url
            FROM products
            WHERE category_id = %s
            ORDER BY product_id ASC
        """, (category_id,))
        
        products = cursor.fetchall()
        return products
    
    except Exception as e:
        print(f"Get products DB error: {e}")
        return []
    
    finally:
        if conn:
            release_db_connection(conn)

def add_product(product_name: str, 
                description: str, 
                price: float, 
                image_url: str,
                category_id: int):
    conn = None

    try:
        conn = get_db_connection()
        cursor = conn.cursor()

        cursor.execute("""
            SELECT product_id 
            FROM products 
            WHERE product_name = %s
        """, (product_name,))
        if cursor.fetchone():
            return False, f"Sản phẩm '{product_name}' đã tồn tại"

        cursor.execute("""
            INSERT INTO products (product_name, description, price, image_url, category_id)
            VALUES (%s, %s, %s, %s, %s)
        """, (product_name, description, price, image_url, category_id))
        
        conn.commit()
        return True, "Thêm sản phẩm thành công."
    
    except Exception as e:
        print(f"Add product DB error: {e}")
        return False, "Đã xảy ra lỗi khi thêm sản phẩm vào cơ sở dữ liệu."
    
    finally:
        if conn:
            release_db_connection(conn)