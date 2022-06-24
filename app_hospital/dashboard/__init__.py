from flask import Blueprint

dashboard_bp = Blueprint('dashboard_bp', __name__, template_folder='templates', static_folder='static')

from app_hospital.dashboard import view_dashboard