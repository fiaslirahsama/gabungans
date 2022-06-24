# memberi nama blueprint folder member untuk digunakan pada view
from flask import Blueprint

bp_member = Blueprint('member', __name__, template_folder='templates', static_folder='static')

from app_perpus.member import member_view