from flask import Blueprint

pasien_bp = Blueprint('pasien_bp', __name__, template_folder='templates', static_folder='static')

from app_hospital.pasien import view_pasien