# memberi nama blueprint folder auth untuk digunakan pada view
from flask import Blueprint

bp_auth = Blueprint('auth', __name__, template_folder='templates', static_folder='static')

from app_perpus.auth import auth_view