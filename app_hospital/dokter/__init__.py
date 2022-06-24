from flask import Blueprint

dokter_bp = Blueprint('dokter_bp', __name__, template_folder='templates', static_folder='static')

from app_hospital.dokter import view_dokter