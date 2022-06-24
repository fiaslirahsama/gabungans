from flask import *
from app_hospital.trans.model_trans import trans
from app_hospital.dokter.model_dokter import dokter
from app_hospital.pasien.model_pasien import pasien
from app_hospital import db, login_user, logout_user, login_required, current_user
import datetime

def viewTrans():
    try:
        rows = db.session.query(trans).join(dokter).join(pasien).filter(trans.flag=="Y").with_entities(trans.id_trans, dokter.id_dokter, dokter.nama_dokter, pasien.no_pasien, pasien.nama_pasien, trans.keluhan, trans.status_bayar, trans.resep_dokter, trans.created_date, trans.updated_date, trans.harga_bayar).all()
        db.session.close()
        return rows
    except Exception as e:
        return flash(e)

def searchTrans():
    try:
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
        db.session.close()
        return rows
    except Exception as e:
        return flash(e)

def showDokter():
    try:
        id_dokter = request.form.get("idDokter")
        nama_dokter = request.form.get("namaDokter")
        hari_kerja = request.form.get("hariKerja")
        jam_kerja = request.form.get("jamKerja")
        availableDokter = dokter.query.filter(dokter.flag=="Y", dokter.kuota!=0)
        db.session.close()
        return availableDokter
    except Exception as e:
        return flash(e)

def searchAvailableDokter():
    try:
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
        availableDokter = dokter.query.filter(dokter.id_dokter.like(id_dokter), dokter.nama_dokter.like(nama_dokter), dokter.jam_kerja.like(jam_kerja), dokter.hari_kerja.like(hari_kerja), dokter.flag=="Y", dokter.kuota!=0).all()
        return availableDokter
        db.session.close()
    except Exception as e:
        return flash(e)

def bookDokter():
    try:
        data = pasien.query.filter(pasien.username==current_user.username).first()
        if data.status_diperiksa == "Y":
            flash("Silahkan Selesaikan Administrasi terlebih dahulu.")
        elif data.status_diperiksa == "N":
            id_dokter = request.form.get("idDokter")
            no_pasien = request.form.get("noPasien")
            keluhan = request.form.get("keluhan")
            date = datetime.datetime.now()
            saveTrans = trans(id_dokter=id_dokter, no_pasien=no_pasien, status_bayar="N", status_checking_dokter="N", resep_dokter="", harga_bayar=0, keluhan=keluhan, flag="Y", created_date=date, updated_date=date)
            db.session.add(saveTrans)
            db.session.commit()
            saveDokter = dokter.query.filter(dokter.id_dokter==id_dokter).first()
            saveDokter.kuota = saveDokter.kuota - 1
            db.session.commit()
            savePasien = pasien.query.filter(pasien.no_pasien==no_pasien).first()
            savePasien.status_diperiksa = "Y"
            db.session.commit()
            return flash("Proses Book Dokter telah Berhasil.")
            db.session.close()
    except Exception as e:
        return flash(e)

def showDokterTrans():
    try:
        rows = db.session.query(trans).join(dokter).join(pasien).filter(trans.flag=="Y", trans.status_bayar=="N", trans.status_checking_dokter=="N").with_entities(trans.id_trans, dokter.id_dokter, dokter.nama_dokter, dokter.hari_kerja, dokter.jam_kerja, pasien.no_pasien, pasien.nama_pasien, trans.keluhan, trans.status_bayar, trans.resep_dokter, trans.created_date, trans.updated_date).all()
        db.session.close()
        return rows
    except Exception as e:
        return flash(e)

# The function below work for searching data from the website and showing the data that has transaction from database.
# This function using form to get value from the website.
def searchDokterInTrans():
    try:
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
        db.session.close()
        return rows
    except Exception as e:
        return flash(e)

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
    saveTrans.updated_date = datetime.datetime.now()
    db.session.commit()
    saveDokter = dokter.query.filter(dokter.id_dokter==id_dokter).first()
    saveDokter.kuota = saveDokter.kuota + 1
    db.session.commit()
    db.session.close()
    return flash("Data Pembayaran Berhasil diinput.")

def paymentList():
    try:
        rows = db.session.query(trans).join(dokter).join(pasien).filter(trans.flag=="Y", trans.status_bayar=="N", trans.status_checking_dokter=="Y").with_entities(trans.id_trans, dokter.id_dokter, dokter.nama_dokter, dokter.hari_kerja, dokter.jam_kerja, pasien.no_pasien, pasien.nama_pasien, trans.keluhan, trans.status_bayar, trans.resep_dokter, trans.created_date, trans.updated_date, trans.harga_bayar).all()
        return rows
    except Exception as e:
        return flash(e)

def searchPayment():
    no_pasien = request.form.get("no_pasien1")
    nama_pasien = request.form.get("nama_pasien1")
    print(no_pasien)
    if no_pasien == "":
        no_pasien = "%"
    else:
        no_pasien = no_pasien
    if nama_pasien == "":
        nama_pasien = "%"
    else:
        nama_pasien = "%"+nama_pasien+"%"
    rows = db.session.query(trans).join(dokter).join(pasien).filter(trans.flag=="Y", trans.status_bayar=="N", trans.status_checking_dokter=="Y", trans.no_pasien.like(no_pasien), pasien.nama_pasien.like(nama_pasien)).with_entities(trans.id_trans, dokter.id_dokter, dokter.nama_dokter, dokter.hari_kerja, dokter.jam_kerja, pasien.no_pasien, pasien.nama_pasien, trans.keluhan, trans.status_bayar, trans.resep_dokter, trans.created_date, trans.updated_date, trans.harga_bayar).all()
    return rows

# The function below work for saving payment status from N to Y value.
# This function using form to get value from the website.
def savePayment():
    try:
        id_trans = request.form.get("idTrans")
        no_pasien = request.form.get("noPasien")
        savePayment = trans.query.filter(trans.id_trans==id_trans, trans.flag=="Y").first()
        savePayment.status_bayar = "Y"
        savePayment.updated_date = datetime.datetime.now()
        db.session.commit()
        savePasien = pasien.query.filter(pasien.no_pasien==no_pasien).first()
        savePasien.status_diperiksa = "N"
        db.session.commit()
        return flash("Pembayaran Berhasil.")
        db.session.close()
    except Exception as e:
        return flash(e)

def detailBookPasien():
    user = current_user.username
    rows = db.session.query(trans).join(pasien).join(dokter).filter(pasien.username==user).with_entities(trans.id_trans, pasien.no_pasien, pasien.nama_pasien, pasien.status_diperiksa, dokter.nama_dokter, dokter.kuota, trans.keluhan, trans.status_bayar, trans.harga_bayar, trans.resep_dokter, trans.status_checking_dokter).order_by(trans.id_trans.desc()).all()
    return rows
    db.session.close()

def checkingDokter():
    try:
        user = current_user.username
        rows = db.session.query(trans).join(dokter).join(pasien).filter(dokter.username==user, trans.flag=="Y", trans.status_bayar=="N", trans.status_checking_dokter=="N").with_entities(trans.id_trans, dokter.id_dokter, dokter.nama_dokter, dokter.hari_kerja, dokter.jam_kerja, pasien.no_pasien, pasien.nama_pasien, trans.keluhan, trans.status_bayar, trans.resep_dokter, trans.created_date, trans.updated_date).all()
        db.session.close()
        return rows
    except Exception as e:
        return flash(e)