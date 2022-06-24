from flask import Blueprint

trans_bp = Blueprint('trans_bp', __name__, template_folder='templates', static_folder='static')

from app_hospital.trans import view_trans