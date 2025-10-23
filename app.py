from flask import Flask, request
from flask_cors import CORS
from routes.admin_routes import admin_route
from routes.auth_routes import auth_route
from db import close_all_connections
import os

app = Flask(__name__)

app.secret_key = os.urandom(24)

CORS(app, resources={
    r"/api/*": {
        "origins": "*",
        "methods": ["GET", "POST", "PUT", "DELETE"],
        "allow_headers": ["Content-Type"]
    }
})

app.register_blueprint(admin_route, url_prefix='/admin')
app.register_blueprint(auth_route, url_prefix='/api')

if __name__ == '__main__':
    try:
        app.run(host='0.0.0.0', port=5000, debug=True)
    finally:
        close_all_connections()