from flask import Blueprint
import os

# 1. ĐỊNH NGHĨA BLUEPRINTS
basedir = os.path.abspath(os.path.dirname(__file__))
admin_route = Blueprint('admin_route', __name__, 
                        static_folder=os.path.join(basedir, '..', 'admin', 'static'), 
                        template_folder=os.path.join(basedir, '..', 'admin', 'views'))

from . import route