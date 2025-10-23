import psycopg2
from psycopg2 import pool

# Cấu hình kết nối PostgreSQL
DB_CONFIG = {
    'host': 'localhost',      
    'database': 'home_made_coffee',
    'user': 'postgres',    
    'password': '38342318',
    'port': '5432'
}

try:
    connection_pool = psycopg2.pool.SimpleConnectionPool(
        1, 10,
        **DB_CONFIG
    )
    if connection_pool:
        print("PostgreSQL connection pool created successfully")
except Exception as e:
    print("Error while connecting to PostgreSQL:", e)


def get_db_connection():
    """Lấy một kết nối từ pool"""
    return connection_pool.getconn()


def release_db_connection(conn):
    """Trả kết nối về pool"""
    connection_pool.putconn(conn)


def close_all_connections():
    """Đóng tất cả kết nối khi server tắt"""
    connection_pool.closeall()
