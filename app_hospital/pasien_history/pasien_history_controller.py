from flask import *
from app_hospital.pasien_history.pasien_history_model import pasien_history
from app_hospital.pasien import pasien_bp
from app_hospital import db
import datetime

# The function below work for showing the active data on the database.
def addPasienHistory(idPasien, nama_pasien, alamat_pasien, updated_date):
    saveAdd = pasien_history(no_pasien=idPasien, nama_pasien=nama_pasien, alamat_pasien=alamat_pasien, flag="Y", updated_date=updated_date, created_date=updated_date)
    db.session.add(saveAdd)
    db.session.commit()
    return redirect(url_for('pasien_bp.viewPasien'))
    db.session.close()

# The function below work for adding data to the database.
# This function use form to get value form the website.
def viewPasienHistory():
    rows = pasien_history.query.filter(pasien_history.flag=="Y")
    return render_template("pasien_history.view_pasien_history.html", datas = rows)