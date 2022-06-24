# Berisi routing untuk menjalankan fungsi controller menggunakan url
from app_perpus.auth import bp_auth, auth_controller
from flask import request, render_template

# REGISTER ADMIN
@bp_auth.route('/register', methods=('GET', 'POST'))
def register():
    return auth_controller.register()

# LOGIN
@bp_auth.route('/login', methods=('GET', 'POST'))
def login():
    return auth_controller.login()

# KIRIM ADMIN ID PADA FRONT END (JINJA2) SETELAH LOGIN
@bp_auth.before_app_request
def load_logged_in_user():
    return auth_controller.load_logged_in_user()

# LOGOUT
@bp_auth.route('/logout')
def logout():
    return auth_controller.logout()