from flask import Flask
from db import get_db_connection, release_db_connection

def get_users():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT user_id, email, password, full_name, phone, created_at
        FROM users
    """)

    users = cursor.fetchall()
    release_db_connection(conn)

    user_list = []
    for user in users:
        user_list.append({
            'user_id': user[0],
            'email': user[1],
            'full_name': user[3],
            'phone': user[4],
            'created_at': user[5]
        })
    
    return user_list