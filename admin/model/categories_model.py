from db import get_db_connection, release_db_connection
from psycopg2.extras import DictCursor

def get_categories():
    """
    Lấy danh sách tất cả các danh mục từ cơ sở dữ liệu.
    Trả về một danh sách các dictionary.
    """
    conn = None

    try:
        conn = get_db_connection()
        # Sử dụng DictCursor để có thể truy cập các cột bằng tên, ví dụ: c['category_name']
        cursor = conn.cursor(cursor_factory=DictCursor)
        
        cursor.execute("""
            SELECT category_id, category_name, description
            FROM categories
            ORDER BY category_id ASC 
        """)
        
        categories = cursor.fetchall()
        return categories
    
    except Exception as e:
        print(f"Get categories DB error: {e}")
        return []
    
    finally:
        if conn:
            release_db_connection(conn)

def get_category_by_id(category_id: int):
    """
    Lấy thông tin danh mục dựa trên category_id.
    Trả về một dictionary hoặc None nếu không tìm thấy.
    """
    conn = None

    try:
        conn = get_db_connection()
        cursor = conn.cursor(cursor_factory=DictCursor)

        cursor.execute("""
            SELECT category_id, category_name, description
            FROM categories
            WHERE category_id = %s
        """, (category_id,))
        
        category = cursor.fetchone()
        return category
    
    except Exception as e:
        print(f"Get category by ID DB error: {e}")
        return None
    
    finally:
        if conn:
            release_db_connection(conn)

def add_category(category_name: str, description: str):
    """
    Thêm một danh mục mới vào cơ sở dữ liệu.
    """
    conn = None

    try:
        conn = get_db_connection()
        cursor = conn.cursor()

        cursor.execute("""
            SELECT category_id 
            FROM categories 
            WHERE category_name = %s
        """, (category_name,))
        if cursor.fetchone():
            return False, f"Danh mục '{category_name}' đã tồn tại"

        cursor.execute("""
            INSERT INTO categories (category_name, description)
            VALUES (%s, %s)
        """, (category_name, description,))
        
        conn.commit()
        return True, "Thêm danh mục thành công"
    
    except Exception as e:
        if conn:
            conn.rollback()
        print(f"Add category DB error: {e}")
        return False, "Đã xảy ra lỗi khi thêm danh mục vào cơ sở dữ liệu."
    
    finally:
        if conn:
            release_db_connection(conn)

def delete_category(category_id: int):
    """
    Xóa một danh mục khỏi cơ sở dữ liệu dựa vào category_id.
    Trả về một tuple (success, message).
    """
    conn = None

    try:
        conn = get_db_connection()
        cursor = conn.cursor()

        cursor.execute("""
            DELETE FROM categories WHERE category_id = %s
        """, (category_id,))
        
        if cursor.rowcount == 0:
            return False, "Không tìm thấy danh mục để xóa."
            
        conn.commit() # Lưu thay đổi
        return True, "Xóa danh mục thành công."
    
    except Exception as e:
        if conn:
            conn.rollback()
        print(f"Delete category DB error: {e}")
        return False, "Đã xảy ra lỗi khi xóa. Danh mục này có thể đang được sử dụng."
    
    finally:
        if conn:
            release_db_connection(conn)

