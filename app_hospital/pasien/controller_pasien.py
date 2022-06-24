from flask import *
from app_hospital.pasien.model_pasien import pasien
from app_hospital import db, current_user, generate_password_hash
from app_hospital.auth import controller_auth
from app_hospital.pasien_history import controller_pasien_history
from app_hospital.auth.model_auth import auth
import datetime

def viewPasien():
    try:
        view = pasien.query.filter(pasien.flag=='Y').all()
        return view
    except Exception as e:
        return flash(e)

def searchPasien():
    no_pasien = request.form.get('no_pasien1')
    nama_pasien = request.form.get('nama_pasien1')
    if no_pasien == '':
        no_pasien = '%'
    else:
        no_pasien = no_pasien
    if nama_pasien == '':
        nama_pasien = '%'
    else:
        nama_pasien = '%'+nama_pasien+'%'
    search = pasien.query.filter(pasien.flag=='Y', pasien.no_pasien.like(no_pasien), pasien.nama_pasien.like(nama_pasien)).all()
    return search

def addPasien():
    status_auth = 'pasien'
    username = request.form.get('username1')
    password = request.form.get('password1')
    nama_pasien = request.form.get('nama_pasien1')
    alamat = request.form.get('alamat_pasien1')
    date = datetime.datetime.now()
    newUser = auth(username=username, status_auth=status_auth, password=generate_password_hash(password, method='sha256'), flag="Y", created_date=date, updated_date=date)
    db.session.add(newUser)
    db.session.commit()
    id_auth = controller_auth.findIdAuth(username)
    add = pasien(id_auth=id_auth, username=username, password=password, nama_pasien=nama_pasien, alamat_pasien=alamat, flag="Y", status_diperiksa='N', created_date=date, updated_date=date)
    db.session.add(add)
    db.session.commit()
    db.session.close()
    return flash("Data Pasien Berhasil Ditambahkan.")

def editPasien(no_pasien):
    no_pasien = request.form.get('no_pasien1')
    username = request.form.get('username1')
    password = request.form.get('password1')
    nama_pasien = request.form.get('nama_pasien1')
    alamat = request.form.get('alamat_pasien1')
    edit = pasien.query.filter(pasien.no_pasien==no_pasien, pasien.flag=='Y').first()
    controller_pasien_history.addPasienHistory(edit.no_pasien, edit.username, edit.nama_pasien, edit.alamat_pasien)
    edit.username = username
    edit.password = password
    edit.nama_pasien = nama_pasien
    edit.alamat_pasien = alamat
    edit.updated_date = datetime.datetime.now()
    db.session.commit()
    saveAuth = auth.query.filter(auth.id_auth==edit.id_auth)
    saveAuth.username = username
    saveAuth.password = generate_password_hash(password, method='sha256')
    db.session.commit()
    db.session.close()
    return flash("Data Pasien Behasil di Update.")

def deletePasien(no_pasien):
    try:
        delete = pasien.query.filter(pasien.no_pasien==no_pasien, pasien.flag=='Y').first()
        delete.flag = 'N'
        delete.updated_date = datetime.datetime.now()
        db.session.commit()
        saveAuth = auth.query.filter(auth.username==delete.username).first()
        saveAuth.flag = "N"
        db.session.commit()
        db.session.close()
        return flash("Data Pasien Berhasil di Hapus.")
    except Exception as e:
        return flash(e)

def findPasienWithUsername(username):
    try:
        rows = pasien.query.filter(pasien.username==username).first()
        db.session.close()
        return rows
    except Exception as e:
        return flash(e)