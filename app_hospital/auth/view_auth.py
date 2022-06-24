from flask import render_template, redirect, request, url_for, flash
from app_hospital.auth import controller_auth, model_auth, auth_bp
from app_hospital.admin import controller_admin
from app_hospital.pasien import controller_pasien
from app_hospital.auth.model_auth import auth
from app_hospital import login_required
from app_hospital import generate_password_hash, check_password_hash, logout_user, current_user, login_user

@auth_bp.route('/')
def form_login():
    return render_template('auth/login.html')

@auth_bp.route('/login', methods=['POST'])
def login():
    username = request.form.get("username1")
    password = request.form.get("password1")
    rows = auth.query.filter(auth.username==username).first()
    if not rows:
        flash("Username tidak tersedia.")
        return redirect(url_for('auth_bp.form_login'))
    elif not check_password_hash(rows.password, password):
        flash("Mohon Cek Username & Password dan coba lagi.")
        return redirect(url_for('auth_bp.form_login'))
    else:
        login_user(user=rows)
        return render_template('dashboard/dashboard.html', username=current_user)

@auth_bp.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('auth_bp.form_login'))

@auth_bp.route('/regis_admin', methods=['POST',  'GET'])
def regis_admin():
    controller_admin.addAdmin()
    return redirect(url_for('auth_bp.form_login'))

@auth_bp.route('/regis_pasien', methods=['POST'])
def regis_pasien():
    controller_pasien.addPasien()
    return redirect(url_for('auth_bp.form_login'))


    