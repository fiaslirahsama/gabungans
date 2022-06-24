# Berisi fungsi-fungsi untuk menjalankan program auth
import functools

from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for
)
from werkzeug.security import check_password_hash, generate_password_hash
from app_perpus import db
from app_perpus.auth.auth_model import admin_perpus

# FUNGSI REGISTRASI ADMIN
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        nama = request.form['nama']
        message = ''

        if not username:
            message = "Masukkan username"
        elif not password:
            message = "Masukkan password"
        elif not nama:
            message = "Masukkan nama"

        if not message:
            insertData = admin_perpus(username=username, password=generate_password_hash(password, method='sha256'), nama=nama)
            cekDataAdmin = admin_perpus.query.filter_by(username=username).all()

            if cekDataAdmin:
                message = f"User {username} telah terdaftar."
            else:   
                db.session.add(insertData)
                db.session.commit()
                message = "Pendaftaran Admin Berhasil."
                flash(message, category="flash-ok")
                return redirect(url_for('auth.login'))
                db.session.close()
        else:
            flash(message, category="flash-error")
    return render_template('auth/register.html')

# FUNGSI LOGIN ADMIN
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        message = ''
        cekAdmin = admin_perpus.query.filter_by(username=username).first()

        if not cekAdmin:
            message = 'Username salah/ tidak terdaftar, silahkan coba lagi'
        elif not check_password_hash(cekAdmin.password, password):
            message = 'Password salah, silahkan coba lagi.'

        if not message:
            session.clear()
            session['admin_id'] = cekAdmin.id
            return redirect(url_for('index'))

        flash(message, category="flash-error")

    return render_template('auth/login.html')

# FUNGSI KIRIM ID ADMIN KE FRONT END
def load_logged_in_user():
    admin_id = session.get('admin_id')

    if not admin_id:
        g.admin = None
    else:
        g.admin = admin_perpus.query.filter_by(id=admin_id).first()

# FUNGSI LOGOUT ADMIN
def logout():
    session.clear()
    return redirect(url_for('index'))

# FUNGSI MENAMPILKAN MENU APABILA TELAH LOGIN
def login_required(view):
    @functools.wraps(view)
    def wrapped_view(**kwargs):
        if not g.admin:
            return redirect(url_for('auth.login'))

        return view(**kwargs)

    return wrapped_view