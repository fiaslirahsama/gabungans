from flask import *
from app_hospital.dokter_history.model_dokter_history import dokter_history
from app_hospital import db
import datetime

def addDokterHistory(id_dokter, username, nama_dokter, hari_kerja, jam_kerja, kuota):
    date = datetime.datetime.now()
    save = dokter_history(id_dokter=id_dokter, username=username, nama_dokter=nama_dokter, hari_kerja=hari_kerja, jam_kerja=jam_kerja, kuota=kuota, flag='Y', created_date=date)
    db.session.add(save)
    db.session.commit()