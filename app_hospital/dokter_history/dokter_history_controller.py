from flask import *
from app_hospital.dokter_history.dokter_history_model import dokter_history
from app_hospital.dokter import dokter_bp
from app_hospital import db
import datetime

# The function below work for showing the active data on the database.
def viewDokterHistory():
    rows = dokter_history.query.filter(dokter_history.flag=="Y")
    return render_template("dokter_history/dokter_history.html", datas=rows)
    db.session.close()

# The function below work for adding data to the database.
# This function use form to get value form the website.
def addDokterHistory(uid, nama_dokter, hari_kerja, jam_kerja, updated_date):
    saveAdd = dokter_history(id_dokter=uid, nama_dokter=nama_dokter, hari_kerja=hari_kerja, jam_kerja=jam_kerja, created_date=updated_date, flag="Y", status_pemeriksaan="N")
    db.session.add(saveAdd)
    db.session.commit()
    return redirect(url_for('dokter_bp.viewDokter'))
    db.session.close()