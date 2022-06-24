# Berisi fungsi-fungsi untuk menjalankan program transaksi
from flask import(
    Blueprint, flash, g, redirect, render_template, request, url_for, make_response
)
import os
from os.path import join, dirname, realpath
from werkzeug.exceptions import abort
import time
from datetime import datetime, timedelta
from io import StringIO
import csv
from app_perpus import db
from app_perpus.auth.auth_model import admin_perpus
from app_perpus.buku.buku_model import buku
from app_perpus.member.member_model import member
from app_perpus.transaksi.transaksi_model import transaksi

# FUNGSI MENAMPILKAN DATA TRANSAKSI
def index():
    transaksis, cp, cj, cw1, cw2 = searchtransaksi()
    # bukus = db.session.query(member.idmember).filter_by(idmember=generateid).first()
    # members
    return transaksis, cp, cj, cw1, cw2


# FUNGSI PENCARIAN DATA TRANSAKSI
def searchtransaksi():
    cp = cj = cw1 = cw2 = ''
    transaksisearch = []
    transaksisearch = db.session.query(transaksi).join(buku).join(member).join(admin_perpus).filter(transaksi.flag == "on").with_entities(transaksi.id, member.nama, buku.judul, transaksi.tgl_pinjam, transaksi.tgl_kembali, admin_perpus.nama, transaksi.flag).all()
    
    if request.method == 'POST':
        if 'caridatatransaksi' in request.form:
            caripeminjam = cp = request.form['caripeminjam']
            carijudul = cj = request.form['carijudul']
            cariwaktu1 = cw1 = request.form['cariwaktu1']
            cariwaktu2 = cw2 = request.form['cariwaktu2']

            if not cw1 and not cw2:
                cp = "%"+str(caripeminjam)+"%"
                cj = "%"+str(carijudul)+"%"
                transaksisearch = db.session.query(transaksi).join(buku).join(member).join(admin_perpus).filter(member.nama.like(cp), buku.judul.like(cj), transaksi.flag == "on").with_entities(transaksi.id, member.nama, buku.judul, transaksi.tgl_pinjam, transaksi.tgl_kembali, admin_perpus.nama, transaksi.flag).all()
            elif not cw1 and cw2:
                cp = "%"+str(caripeminjam)+"%"
                cj = "%"+str(carijudul)+"%"
                transaksisearch = db.session.query(transaksi).join(buku).join(member).join(admin_perpus).filter(member.nama.like(cp), buku.judul.like(cj), transaksi.tgl_kembali <= cw2, transaksi.flag == "on").with_entities(transaksi.id, member.nama, buku.judul, transaksi.tgl_pinjam, transaksi.tgl_kembali, admin_perpus.nama, transaksi.flag).all()
            elif cw1 and not cw2:
                cp = "%"+str(caripeminjam)+"%"
                cj = "%"+str(carijudul)+"%"
                transaksisearch = db.session.query(transaksi).join(buku).join(member).join(admin_perpus).filter(member.nama.like(cp), buku.judul.like(cj), transaksi.tgl_kembali >= cw1, transaksi.flag == "on").with_entities(transaksi.id, member.nama, buku.judul, transaksi.tgl_pinjam, transaksi.tgl_kembali, admin_perpus.nama, transaksi.flag).all()
            elif cw1 and cw2:
                cp = "%"+str(caripeminjam)+"%"
                cj = "%"+str(carijudul)+"%"
                transaksisearch = db.session.query(transaksi).join(buku).join(member).join(admin_perpus).filter(member.nama.like(cp), buku.judul.like(cj), transaksi.tgl_kembali.between(cw1, cw2), transaksi.flag == "on").with_entities(transaksi.id, member.nama, buku.judul, transaksi.tgl_pinjam, transaksi.tgl_kembali, admin_perpus.nama, transaksi.flag).all()
                
    return transaksisearch, cp, cj, cw1, cw2

# FUNGSI MENAMBAH DATA TRANSAKSI PEMINJAMAN BUKU
def tambahtransaksi():
    message = []
    if request.method == 'POST':
        idmember = request.form['idmember']
        kodebukuin = request.form['kodebuku']
        jumlah_hari = request.form['jumlah_hari']
        idadmin = request.form['idadmin']
        created_by = request.form['created_by']
        trans_ok_count = trans_fail_count = 0
        kodebukulist = kodebukuin.split(';')
        print(kodebukulist)
        for kodebuku in kodebukulist:
            error = False
            print(kodebuku, idmember, idadmin, jumlah_hari)
            datamember = db.session.query(member.idmember).filter_by(idmember=idmember).first()
            databuku = db.session.query(buku.judul).filter_by(kodebuku=kodebuku).first()
            datapinjam = db.session.query(buku.kodebuku).filter_by(kodebuku=kodebuku, status='ada').first()
            print(databuku)

            if not idmember:
                error = True
                message.append('masukkan id member')
            elif not kodebuku:
                error = True
                message.append('masukkan kode buku')
            elif not jumlah_hari:
                error = True
                message.append('masukkan tanggal pengembalian')
            elif not databuku and not datamember:
                error = True
                message.append('Data member '+idmember+' dan buku '+kodebuku+' tidak ditemukan')
            elif not datamember:
                error = True
                message.append('Data member '+idmember+' tidak ditemukan')
            elif databuku and not datapinjam:
                error = True
                for i in databuku:
                    judulbuku = i
                message.append('Buku ' + str(judulbuku) + ' sedang dipinjam')
            elif not databuku:
                error = True
                message.append('Data buku '+kodebuku+' tidak ditemukan')
        
            if not error:
                trans_ok_count = trans_ok_count + 1
                tgl_kembali = datetime.now().date() + timedelta(days=int(jumlah_hari))
                insertData = transaksi(idmember=idmember, kodebuku=kodebuku, tgl_kembali=tgl_kembali, idadmin=idadmin, created_by=created_by)
                db.session.add(insertData)
                db.session.commit()
                updateData = buku.query.filter_by(kodebuku=kodebuku).first()
                updateData.status = "dipinjam"
                db.session.commit()
                db.session.close()
            else:
                trans_fail_count = trans_fail_count + 1
    
    if trans_ok_count > 0 and trans_fail_count == 0:
        flash('Berhasil menambah '+str(trans_ok_count)+' Transaksi', category="flash-ok")
    elif trans_ok_count == 0 and trans_fail_count > 0:
        flash('Gagal menambah '+str(trans_fail_count)+' transaksi', category="flash-error")
        flash(message, category="flash-error")
    elif trans_ok_count > 0 and trans_fail_count > 0:
        flash('Berhasil menambah '+str(trans_ok_count)+' Transaksi', category="flash-ok")
        flash('Gagal menambah '+str(trans_fail_count)+' transaksi', category="flash-error")
        flash(message, category="flash-error")
    


# FUNGSI MENDAPATKAN DATA TRANSAKSI BERDASARKAN ID
def get_transaksi(id):
    gettransaksi = transaksi.query.filter_by(id=id).first()

    if not gettransaksi:
        abort(404, f"transaksi dengan id {id} tidak ditemukan")

    return gettransaksi

# FUNGSI MENGHAPUS DATA TRANSAKSI APABILA BUKU TELAH DIKEMBALIKAN
def updatetransaksi(id):
    gettransaksi = get_transaksi(id)
    if request.method == 'POST':
        idmember = request.form['idmember']
        kodebuku = request.form['kodebuku']
        tgl_kembali = request.form['tgl_kembali']
        flag = request.form['flag']
        updated_by = request.form['updated_by']
        messagetransaksi = ''

        if not kodebuku:
            messagetransaksi = 'masukkan kode kodebuku'
        elif not idmember:
            messagetransaksi = 'masukkan id member'
        elif not tgl_kembali:
            messagetransaksi = 'masukkan tanggal kembali'

        if not messagetransaksi:
            updateDataBuku = buku.query.filter_by(kodebuku=kodebuku).first()
            updateDataBuku.status = "ada"
            db.session.commit()
            updateDataTransaksi = transaksi.query.filter_by(id=id).first()
            updateDataTransaksi.updated_at = datetime.now()
            updateDataTransaksi.updated_by = updated_by
            updateDataTransaksi.flag = flag
            db.session.commit()
            db.session.close()
            flash('Buku Berhasil Dikembalikan', category="flash-ok")
            renderself = False
            return renderself, gettransaksi
        else:
            flash(messagetransaksi, category="flash-error")
            renderself = True
            return renderself, gettransaksi
    else:
        renderself = True
        return renderself, gettransaksi

# FUNGSI DOWNLOAD/EXPORT DATA TRANSAKSI DENGAN FORMAT CSV
def downloadtransaksi():
    cp = cj = cw1 = cw2 = ''
    transaksicsv = []
    transaksicsv = db.session.query(transaksi).join(buku).join(member).join(admin_perpus).filter(transaksi.flag == "on").with_entities(member.nama, buku.judul, transaksi.tgl_pinjam, transaksi.tgl_kembali, admin_perpus.nama).all()
    
    if request.method == 'POST':
        if 'downloaddatatransaksi' in request.form:
            caripeminjam = cp = request.form['cp']
            carijudul = cj = request.form['cj']
            cariwaktu1 = cw1 = request.form['cw1']
            cariwaktu2 = cw2 = request.form['cw2']
            if cw1 == 'None':
                cw1 = ''
            elif cw2 == 'None':
                cw2 = ''

            if not cw1 and not cw2:
                cp = "%"+str(caripeminjam)+"%"
                cj = "%"+str(carijudul)+"%"
                transaksicsv = db.session.query(transaksi).join(buku).join(member).join(admin_perpus).filter(member.nama.like(cp), buku.judul.like(cj), transaksi.flag == "on").with_entities(member.nama, buku.judul, transaksi.tgl_pinjam, transaksi.tgl_kembali, admin_perpus.nama).all()
            elif not cw1 and cw2:
                cp = "%"+str(caripeminjam)+"%"
                cj = "%"+str(carijudul)+"%"
                transaksicsv = db.session.query(transaksi).join(buku).join(member).join(admin_perpus).filter(member.nama.like(cp), buku.judul.like(cj), transaksi.tgl_kembali <= cw2, transaksi.flag == "on").with_entities(member.nama, buku.judul, transaksi.tgl_pinjam, transaksi.tgl_kembali, admin_perpus.nama).all()
            elif cw1 and not cw2:
                cp = "%"+str(caripeminjam)+"%"
                cj = "%"+str(carijudul)+"%"
                transaksicsv = db.session.query(transaksi).join(buku).join(member).join(admin_perpus).filter(member.nama.like(cp), buku.judul.like(cj), transaksi.tgl_kembali >= cw1, transaksi.flag == "on").with_entities(member.nama, buku.judul, transaksi.tgl_pinjam, transaksi.tgl_kembali, admin_perpus.nama).all()
            elif cw1 and cw2:
                cp = "%"+str(caripeminjam)+"%"
                cj = "%"+str(carijudul)+"%"
                transaksicsv = db.session.query(transaksi).join(buku).join(member).join(admin_perpus).filter(member.nama.like(cp), buku.judul.like(cj), transaksi.tgl_kembali.between(cw1, cw2), transaksi.flag == "on").with_entities(member.nama, buku.judul, transaksi.tgl_pinjam, transaksi.tgl_kembali, admin_perpus.nama).all()

    export_transaksi = ['NAMA PEMINJAM', 'JUDUL BUKU', 'TANGGAL PINJAM', 'TANGGAL KEMBALI', 'NAMA ADMIN']
    si = StringIO()
    cw = csv.writer(si)
    cw.writerow(export_transaksi)
    cw.writerows(transaksicsv)
    output = make_response(si.getvalue())
    output.headers["Content-Disposition"] = "attachment; filename=datatransaksi.csv"
    output.headers["Content-type"] = "text/csv"
    return output