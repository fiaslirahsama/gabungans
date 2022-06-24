from flask import *
from app_hospital.pasien_history.model_pasien_history import pasien_history
from app_hospital import db
import datetime

def addPasienHistory(no_pasien, username, nama_pasien, alamat):
    date = datetime.datetime.now()
    save = pasien_history(no_pasien=no_pasien, username=username, nama_pasien=nama_pasien, alamat_pasien=alamat, flag='Y', updated_date=date, created_date=date)
    db.session.add(save)
    db.session.commit()