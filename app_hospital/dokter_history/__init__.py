from flask import Blueprint

dokter_history_bp = Blueprint('dokter_history_bp', __name__, template_folder='templates', static_folder='static')

from app_hospital.dokter_history import view_dokter_history