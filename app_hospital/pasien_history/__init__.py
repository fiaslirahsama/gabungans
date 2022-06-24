from flask import Blueprint

pasien_history_bp = Blueprint('pasien_history_bp', __name__, template_folder='templates', static_folder='static')

from app_hospital.pasien_history import view_pasien_history