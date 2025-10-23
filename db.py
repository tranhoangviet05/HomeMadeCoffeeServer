import psycopg2
from psycopg2.pool import SimpleConnectionPool
import os
import sys

# Cấu hình kết nối PostgreSQL
# DB_CONFIG = {
#     'host': 'localhost',      
#     'database': 'home_made_coffee',
#     'user': 'postgres',    
#     'password': '38342318',
#     'port': '5432'
# }

# SECRET_KEY: 2fe5b8df217f59edb66f83f7c3f4234f
pool = None

def get_db_connection():
    """
    Lấy một kết nối từ pool.
    Sử dụng "lazy initialization" (khởi tạo lười) để tạo pool
    khi hàm này được gọi lần đầu tiên.
    """
    global pool

    if pool is None:
        try:
            DATABASE_URL = os.environ.get('DATABASE_URL')
            
            if not DATABASE_URL:
                print("Warning: DATABASE_URL not set. Using local fallback.", file=sys.stderr)
                DATABASE_URL = 'postgresql://postgres:38342318@localhost:5432/home_made_coffee'
            
            print("Initializing connection pool...")
            pool = SimpleConnectionPool(
                minconn=1,
                maxconn=10,
                dsn=DATABASE_URL
            )
            print("Connection pool initialized successfully.")
        
        except psycopg2.OperationalError as e:
            print(f"FATAL: Could not initialize connection pool: {e}", file=sys.stderr)
            pool = None
            return None
    
    if pool:
        try:
            return pool.getconn()
        except psycopg2.Error as e:
            print(f"Error getting connection from pool: {e}", file=sys.stderr)
            return None

    print("Error: Connection pool is not available.", file=sys.stderr)
    return None

def release_db_connection(conn):
    """Trả kết nối về cho pool."""
    if pool and conn:
        try:
            pool.putconn(conn)
        except psycopg2.Error as e:
            print(f"Error releasing connection: {e}", file=sys.stderr)

def close_all_connections():
    """Đóng tất cả kết nối trong pool khi ứng dụng tắt."""
    if pool:
        pool.closeall()
        print("All database connections closed.")
