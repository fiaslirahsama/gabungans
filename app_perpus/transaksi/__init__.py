# memberi nama blueprint folder transaksi untuk digunakan pada view

from flask import Blueprint

bp_transaksi = Blueprint('transaksi', __name__, template_folder='templates', static_folder='static')

from app_perpus.transaksi import transaksi_view