from flask import *
from app_hospital.trans.trans_model import trans
from app_hospital.dokter.dokter_model import dokter
from app_hospital.pasien.pasien_model import pasien
from app_hospital import db
import datetime

# This file is work for setting the function

# The function below work for showing the active data on the database.
def viewTrans():
    rows = db.session.query(trans).join(dokter).join(pasien).filter(trans.flag=="Y").with_entities(trans.id_trans, dokter.id_dokter, dokter.nama_dokter, pasien.no_pasien, pasien.nama_pasien, trans.keluhan, trans.status_bayar, trans.resep_dokter, trans.created_date, trans.updated_date, trans.harga_bayar).all()
    return render_template("trans/record_trans.html", datas=rows)
    db.session.close()

# The function below work for searching data from the website and showing active data from database.
# This function using form to get value from the website.
def searchTrans():
    no_pasien = request.form.get("idPasien")
    nama_pasien = request.form.get("namaPasien")
    status_bayar = request.form.get("statusBayar")
    if no_pasien == "":
        no_pasien = "%"
    else:
        no_pasien = no_pasien
    if nama_pasien == "":
        nama_pasien = "%"
    else:
        nama_pasien = "%"+nama_pasien+"%"
    if status_bayar == "":
        status_bayar = "%"
    else:
        status_bayar = status_bayar
    rows = db.session.query(trans).join(dokter).join(pasien).filter(trans.flag=="Y", trans.no_pasien.like(no_pasien), pasien.nama_pasien.like(nama_pasien), trans.status_bayar.like(status_bayar)).with_entities(trans.id_trans, dokter.id_dokter, dokter.nama_dokter, pasien.no_pasien, pasien.nama_pasien, trans.keluhan, trans.status_bayar, trans.resep_dokter, trans.created_date, trans.updated_date, trans.harga_bayar).all()
    return render_template("trans/record_trans.html", datas=rows)
    db.session.close()

# The function below work for showing data that has flag value "Y" and status_pemeriksaan value "N"
# This function work for showing dokter that available and didnt have transaction running.
def showAvailableDokter():
    availableDokter = dokter.query.filter(dokter.flag=="Y", dokter.status_pemeriksaan=="N")
    availablePasien = pasien.query.filter(pasien.flag=="Y")
    return render_template("trans/trans_available_dokter.html", datas=availableDokter, datas2=availablePasien)
    db.session.close()

# The function below work for searching data from the website and showing active data from database.
# This function using form to get value from the website.
def searchAvailableDokter():
    id_dokter = request.form.get("idDokter")
    nama_dokter = request.form.get("namaDokter")
    hari_kerja = request.form.get("hariKerja")
    jam_kerja = request.form.get("jamKerja")
    if id_dokter == "":
        id_dokter = "%"
    else:
        id_dokter = id_dokter
    if nama_dokter == "":
        nama_dokter = "%"
    else:
        nama_dokter = "%" + nama_dokter + "%"
    if jam_kerja == "":
        jam_kerja = "%"
    else:
        jam_kerja = "%" + jam_kerja + "%"
    if hari_kerja == "":
        hari_kerja = "%"
    else:
        hari_kerja = "%" + hari_kerja + "%"
    availableDokter = dokter.query.filter(dokter.id_dokter.like(id_dokter), dokter.nama_dokter.like(nama_dokter), dokter.jam_kerja.like(jam_kerja), dokter.hari_kerja.like(hari_kerja), dokter.flag=="Y").all()
    availablePasien = pasien.query.filter(pasien.flag=="Y")
    return render_template("trans/trans_available_dokter.html", datas=availableDokter, datas2=availablePasien)
    db.session.close()

# The function below work for add transaction to the database using value from website form.
# This function also changing value in the database from dokter table and pasien table. 
def bookDokter():
    id_dokter = request.form.get("idDokter")
    no_pasien = request.form.get("noPasien")
    keluhan = request.form.get("keluhan")
    date = datetime.datetime.now()
    saveTrans = trans(id_dokter=id_dokter, no_pasien=no_pasien, status_bayar="N", status_checking_dokter="N", resep_dokter="", harga_bayar=0, keluhan=keluhan, flag="Y", created_date=date, updated_date=date)
    db.session.add(saveTrans)
    db.session.commit()
    saveDokter = dokter.query.filter(dokter.id_dokter==id_dokter).first()
    saveDokter.status_pemeriksaan = "Y"
    db.session.commit()
    savePasien = pasien.query.filter(pasien.no_pasien==no_pasien).first()
    savePasien.status_diperiksa = "Y"
    db.session.commit()
    flash("Proses Book Dokter telah Berhasil.")
    return redirect(url_for('trans_bp.showAvailableDokter'))
    db.session.close()

# The function below work for showing the data that has transaction from the database.
def showDokterInTrans():
    rows = db.session.query(trans).join(dokter).join(pasien).filter(trans.flag=="Y", trans.status_bayar=="N", trans.status_checking_dokter=="N").with_entities(trans.id_trans, dokter.id_dokter, dokter.nama_dokter, dokter.hari_kerja, dokter.jam_kerja, pasien.no_pasien, pasien.nama_pasien, trans.keluhan, trans.status_bayar, trans.resep_dokter, trans.created_date, trans.updated_date).all()
    return render_template("trans/checking_dokter.html", datas=rows)
    db.session.close()

# The function below work for searching data from the website and showing the data that has transaction from database.
# This function using form to get value from the website.
def searchDokterInTrans():
    id_dokter = request.form.get("idDokter")
    nama_dokter = request.form.get("namaDokter")
    hari_kerja = request.form.get("hariKerja")
    jam_kerja = request.form.get("jamKerja")
    if id_dokter == "":
        id_dokter = "%"
    else:
        id_dokter = id_dokter
    if nama_dokter == "":
        nama_dokter = "%"
    else:
        nama_dokter = "%" + nama_dokter + "%"
    if jam_kerja == "":
        jam_kerja = "%"
    else:
        jam_kerja = "%" + jam_kerja + "%"
    if hari_kerja == "":
        hari_kerja = "%"
    else:
        hari_kerja = "%" + hari_kerja + "%"
    rows = db.session.query(trans).join(dokter).join(pasien).filter(trans.flag=="Y", trans.status_bayar=="N", trans.id_dokter.like(id_dokter), dokter.nama_dokter.like(nama_dokter), dokter.hari_kerja.like(hari_kerja), dokter.jam_kerja.like(jam_kerja)).with_entities(trans.id_trans, dokter.id_dokter, dokter.nama_dokter, dokter.hari_kerja, dokter.jam_kerja, pasien.no_pasien, pasien.nama_pasien, trans.keluhan, trans.status_bayar, trans.resep_dokter, trans.created_date, trans.updated_date).all()
    return render_template("trans/checking_dokter.html", datas=rows)
    db.session.close()

# The function below work for saving transaction to the database using value from website form.
# This function also changing value in the database from dokter table and trans table. 
def saveDokterResult():
    id_trans = request.form.get("idTrans")
    id_dokter = request.form.get("idDokter")
    no_pasien = request.form.get("noPasien")
    resep_dokter = request.form.get("resepDokter")
    keluhan = request.form.get("keluhan")
    harga_bayar = request.form.get("hargaBayar")
    updated_date = datetime.datetime.now()
    saveTrans = trans.query.filter(trans.id_trans==id_trans, trans.flag=="Y").first()
    saveTrans.id_dokter = id_dokter
    saveTrans.no_pasien = no_pasien
    saveTrans.resep_dokter = resep_dokter
    saveTrans.keluhan = keluhan
    saveTrans.harga_bayar = harga_bayar
    saveTrans.status_checking_dokter = "Y"
    db.session.commit()
    saveDokter = dokter.query.filter(dokter.id_dokter==id_dokter).first()
    saveDokter.status_pemeriksaan = "N"
    db.session.commit()
    flash("Data Pembayaran Berhasil diinput.")
    return redirect(url_for('trans_bp.showDokterInTrans'))
    db.session.close()

# The function below work for showing the data that has N value in the trans table on status_bayar column from the database.
def showPaymentList():
    rows = db.session.query(trans).join(dokter).join(pasien).filter(trans.flag=="Y", trans.status_bayar=="N", trans.status_checking_dokter=="Y").with_entities(trans.id_trans, dokter.id_dokter, dokter.nama_dokter, dokter.hari_kerja, dokter.jam_kerja, pasien.no_pasien, pasien.nama_pasien, trans.keluhan, trans.status_bayar, trans.resep_dokter, trans.created_date, trans.updated_date, trans.harga_bayar).all()
    return render_template("trans/payment.html", datas=rows)

# The function below work for searching data from the website and showing the data that has transaction from database.
# This function using form to get value from the website.
def searchPaymentList():
    no_pasien = request.form.get("idPasien")
    nama_pasien = request.form.get("namaPasien")
    if no_pasien == "":
        no_pasien = "%"
    else:
        no_pasien = no_pasien
    if nama_pasien == "":
        nama_pasien = "%"
    else:
        nama_pasien = "%"+nama_pasien+"%"
    rows = db.session.query(trans).join(dokter).join(pasien).filter(trans.flag=="Y", trans.status_bayar=="N", trans.status_checking_dokter=="Y", trans.no_pasien.like(no_pasien), pasien.nama_pasien.like(nama_pasien)).with_entities(trans.id_trans, dokter.id_dokter, dokter.nama_dokter, dokter.hari_kerja, dokter.jam_kerja, pasien.no_pasien, pasien.nama_pasien, trans.keluhan, trans.status_bayar, trans.resep_dokter, trans.created_date, trans.updated_date, trans.harga_bayar).all()
    return render_template("trans/payment.html", datas=rows)

# The function below work for saving payment status from N to Y value.
# This function using form to get value from the website.
def savePayment():
    id_trans = request.form.get("idTrans")
    no_pasien = request.form.get("noPasien")
    savePayment = trans.query.filter(trans.id_trans==id_trans, trans.flag=="Y").first()
    savePayment.status_bayar = "Y"
    db.session.commit()
    savePasien = pasien.query.filter(pasien.no_pasien==no_pasien).first()
    savePasien.status_diperiksa = "N"
    db.session.commit()
    flash("Pembayaran Berhasil.")
    return redirect(url_for('trans_bp.showPaymentList'))
    db.session.close()