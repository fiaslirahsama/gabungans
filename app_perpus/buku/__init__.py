# memberi nama blueprint folder buku untuk digunakan pada view
from flask import Blueprint

bp_buku = Blueprint('buku', __name__, template_folder='templates', static_folder='static')

from app_perpus.buku import buku_view