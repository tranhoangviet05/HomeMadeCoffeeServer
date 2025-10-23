from flask import request, jsonify
from db import get_db_connection, release_db_connection
from api_models.auth_models import get_user_from_email
import hashlib
from datetime import datetime
from admin import auth_route

def hash_password(password):
    """Mã hóa mật khẩu bằng SHA256"""
    return hashlib.sha256(password.encode()).hexdigest()

# LOGIN API
@auth_route.route('/login', methods=['POST'])
def login():
    try:
        data = request.json
        email = data.get('email')
        password = data.get('password')

        # Validate input
        if not email or not password:
            return jsonify({
                'status': 'error', 
                'message': 'Email và mật khẩu không được để trống'
            }), 400
        
        user = get_user_from_email(email)

        if not user:
            return jsonify({
                'status': 'error',
                'message': 'Email không tồn tại'
            }), 401

        password_match = hash_password(password) == user['password']

        if not password_match:
            return jsonify({
                'status': 'error',
                'message': 'Mật khẩu không chính xác'
            }), 401

        # Đăng nhập thành công
        return jsonify({
            'status': 'success',
            'message': 'Đăng nhập thành công',
            'data': {
                'user_id': user['user_id'],
                'email': user['email'],
                'full_name': user['full_name'],
                'phone': user['phone'],
            }
        }), 200

    except Exception as e:
        print(f"Login error: {str(e)}")
        return jsonify({
            'status': 'error',
            'message': 'Đã xảy ra lỗi khi đăng nhập'
        }), 500


# REGISTER API
@auth_route.route('/register', methods=['POST'])
def register():
    try:
        data = request.json
        email = data.get('email')
        password = data.get('password')
        full_name = data.get('full_name')
        phone = data.get('phone')
        created_at = datetime.now()

        # Validate input
        if not email or not password or not full_name:
            return jsonify({
                'status': 'error', 
                'message': 'Vui lòng điền đầy đủ thông tin'
            }), 400

        conn = get_db_connection()
        cursor = conn.cursor()

        # Kiểm tra email đã tồn tại chưa
        cursor.execute("SELECT user_id FROM users WHERE email = %s", (email,))
        if cursor.fetchone():
            release_db_connection(conn)
            return jsonify({
                'status': 'error',
                'message': 'Email đã được sử dụng'
            }), 400

        # Hash mật khẩu trước khi lưu
        hashed_password = hash_password(password)

        # Insert user mới
        cursor.execute("""
            INSERT INTO users (full_name, phone, email, password, created_at)
            VALUES (%s, %s, %s, %s, %s)
            RETURNING user_id, created_at
        """, (full_name, phone, email, hashed_password, created_at))
        
        user_id = cursor.fetchone()[0]
        conn.commit()
        release_db_connection(conn)

        return jsonify({
            'status': 'success',
            'message': 'Đăng ký thành công',
            'data': {
                'user_id': user_id,
            }
        }), 201

    except Exception as e:
        print(f"❌ Register error: {str(e)}")
        if conn:
            conn.rollback()
            release_db_connection(conn)
        return jsonify({
            'status': 'error',
            'message': 'Đã xảy ra lỗi khi đăng ký'
        }), 500


# TEST API - Kiểm tra server có hoạt động không
@auth_route.route('/test', methods=['GET'])
def test():
    return jsonify({
        'status': 'success',
        'message': 'Server is running!'
    }), 200