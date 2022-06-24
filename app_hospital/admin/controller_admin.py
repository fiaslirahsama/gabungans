from app_hospital import db
from flask import *
from app_hospital.admin.model_admin import admin
from app_hospital.admin_history import controller_admin_history
from app_hospital.auth.model_auth import auth
from app_hospital.auth import controller_auth
import datetime
from flask_login import login_user, logout_user, login_required, current_user
from werkzeug.security import generate_password_hash

def viewAdmin():
    try:
        rows = db.session.query(admin).join(auth).filter(auth.status_auth=="admin").all()
        return rows
    except Exception as e:
        return flash(e)

def addAdmin():
    try:
        status_auth = 'admin'
        username = request.form.get("username")
        password = request.form.get("password")
        nama_admin = request.form.get("namaAdmin")
        jabatan = request.form.get("jabatan")
        date = datetime.datetime.now()
        newUser = auth(username=username, status_auth=status_auth, password=generate_password_hash(password, method='sha256'), flag="Y", created_date=date, updated_date=date)
        db.session.add(newUser)
        db.session.commit()
        id = controller_auth.findIdAuth(username)
        saveAdd = admin(id_auth=id, username=username, password=password, nama_admin=nama_admin, jabatan=jabatan, flag="Y", created_date=date, updated_date=date)
        db.session.add(saveAdd)
        db.session.commit()
        saveAuth = auth.query.filter(auth.id_auth==edit.id_auth)
        saveAuth.username = username
        saveAuth.password = generate_password_hash(password, method='sha256')
        db.session.commit()
        db.session.close()
        return flash("Data Successfully Added.")
    except Exception as e:
        return flash(e)

def deleteAdmin(idAdmin):
    try:
        saveDelete = admin.query.filter(admin.id_admin==idAdmin).first()
        saveDelete.flag = "N"
        saveDelete.updated_date = datetime.datetime.now()
        db.session.commit()
        saveAuth = auth.query.filter(auth.username==saveDelete.username).first()
        saveAuth.flag = "N"
        db.session.commit()
        db.session.close()
        return flash("Data Successfully Deleted.")
    except Exception as e:
        return flash(e)

def editAdmin(idAdmin):
    username = request.form.get("username")
    password = request.form.get("password")
    nama_admin = request.form.get("namaAdmin")
    jabatan = request.form.get("jabatan")
    updated_date = datetime.datetime.now()
    saveEditAdmin = admin.query.filter(admin.id_admin==idAdmin).first()
    controller_admin_history.addAdminHistory(idAdmin, saveEditAdmin.username, saveEditAdmin.nama_admin, saveEditAdmin.jabatan)
    saveEditAdmin.nama_admin = nama_admin
    saveEditAdmin.jabatan = jabatan
    saveEditAdmin.username = username
    saveEditAdmin.password = password
    saveEditAdmin.updated_date = updated_date
    saveEditAdmin.flag = "Y"
    db.session.commit()
    db.session.close()
    return flash("Data Successfully Updated.")

def searchAdmin():
    id_admin = request.form.get("id_admin")
    nama_admin = request.form.get("nama_admin")
    if id_admin == "":
        id_admin = "%"
    else:
        id_admin = id_admin
    if nama_admin == "":
        nama_admin = "%"
    else:
        nama_admin = "%" + nama_admin + "%"
    rows = admin.query.filter(admin.id_admin.like(id_admin), admin.nama_admin.like(nama_admin), admin.flag=="Y").all()
    db.session.close()
    return rows