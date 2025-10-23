from db import get_db_connection, release_db_connection
import hashlib
from datetime import datetime
from psycopg2.extras import DictCursor

def hash_password(password):
    """Mã hóa mật khẩu bằng SHA256"""
    return hashlib.sha256(password.encode()).hexdigest()

def get_user_from_email(email: str):
    try:
        conn = get_db_connection()
        cursor = conn.cursor(cursor_factory=DictCursor)

        # Tìm user theo email
        cursor.execute("""
            SELECT user_id, email, password, full_name, phone, created_at 
            FROM users 
            WHERE email = %s
        """, (email,))
        
        user = cursor.fetchone()
        return user

    except Exception as e:
        print(f"Login error: {str(e)}")
        return {
            'status': 'error',
            'message': 'Đã xảy ra lỗi khi đăng nhập'
        }, 500
    
    finally:
        if conn:
            release_db_connection(conn)

def create_user(email: str, password: str, full_name: str, phone: str):
    try:
        conn = get_db_connection()
        cursor = conn.cursor(cursor_factory=DictCursor)

        # Kiểm tra email đã tồn tại chưa
        cursor.execute("SELECT user_id FROM users WHERE email = %s", (email,))
        if cursor.fetchone():
            release_db_connection(conn)
            return False, f"Email '{email}' đã tồn tại"

        hashed_password = hash_password(password)
        created_at = datetime.now()

        cursor.execute("""
            INSERT INTO users (email, password, full_name, phone, created_at)
            VALUES (%s, %s, %s, %s, %s)
        """, (email, hashed_password, full_name, phone, created_at))
        
        conn.commit()
        return True, "Đăng ký thành công"

    except Exception as e:
        if conn:
            conn.rollback()
        print(f"Register error: {str(e)}")
        return False, "Đã xảy ra lỗi khi đăng ký người dùng."
    
    finally:
        if conn:
            release_db_connection(conn)