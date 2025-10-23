from flask import Blueprint
import os

# 1. ĐỊNH NGHĨA BLUEPRINTS
basedir = os.path.abspath(os.path.dirname(__file__))
auth_route = Blueprint('auth_route', __name__)

from . import auth_routes