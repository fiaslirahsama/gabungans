from flask import Blueprint

admin_history_bp = Blueprint('admin_history_bp', __name__, template_folder='templates', static_folder='static')

from app_hospital.admin_history import view_admin_history