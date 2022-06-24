from flask import *
from app_hospital.admin_history.model_admin_history import admin_history
from app_hospital import db
import datetime

def addAdminHistory(id_admin, username, nama_admin, jabatan):
    date = datetime.datetime.now()
    save = admin_history(id_admin=id_admin, username=username, nama_admin=nama_admin, jabatan=jabatan, flag='Y', updated_date=date)
    db.session.add(save)
    db.session.commit()
