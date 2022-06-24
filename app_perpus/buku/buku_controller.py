# Berisi fungsi-fungsi untuk menjalankan program buku
from flask import(
    Blueprint, flash, g, redirect, render_template, request, url_for, make_response, send_file
)
import os, csv, time
from os.path import join, dirname, realpath
from werkzeug.exceptions import abort
from datetime import datetime, timedelta
from io import StringIO
from app_perpus import db
from app_perpus.buku.buku_model import buku, koderak, kodegenre

# Mendefinisikan folder untuk menyimpan file csv buku
BASEDIR = os.path.abspath(os.path.dirname(os.path.dirname(realpath(__file__))))
FOLDER_CSVBUKU = os.path.join(BASEDIR, './static/csvupload/buku/')

# FUNGSI GENERATE 6 DIGIT ANGKA RANDOM UNTUK KODE BUKU
def random():
    import random, math
    digits = [i for i in range(0,10)]
    random_str = ""
    for i in range(6):
        index = math.floor(random.random()*10)
        random_str += str(digits[index])
    return random_str

# FUNGSI MENAMPILKAN DATA BUKU
def dataBuku():
    while True:
        generate_id = random()
        cekid = db.session.query(buku.kodebuku).filter_by(kodebuku=generate_id).first()
        if not cekid:
            break
    
    return generate_id

# FUNGSI MENAMPILKAN DATA KODE RAK BUKU DAN KODE GENRE
def dataKode():
    koderaks = koderak.query.all()
    kodegenres = kodegenre.query.all()
    print(koderaks, kodegenres)
    return koderaks, kodegenres

# FUNGSI MENAMBAHKAN DATA BUKU
def tambahBuku():
    if request.method == 'POST':
        kodebuku = request.form['kodebuku']
        judul = request.form['judul']
        genre = request.form['genre']
        lokasi = request.form['lokasi']
        status = request.form['status']
        created_by = request.form['created_by']
        lenkodebuku = len(kodebuku)
        cekbuku = db.session.query(buku.kodebuku).filter_by(kodebuku=kodebuku).first()
        messagebuku = ''
        if lenkodebuku == 6:
            if not kodebuku:
                messagebuku = 'Masukkan Kode Buku'
            elif not judul:
                messagebuku = 'Masukkan Judul Buku'
            elif not genre:
                messagebuku = 'Masukkan Genre Buku'
            elif not lokasi:
                messagebuku = 'Tulis Lokasi Rak Buku'
            elif cekbuku:
                messagebuku = 'Kode Buku Sudah Terpakai'
            
            if not messagebuku:
                insertData = buku(kodebuku=kodebuku, judul=judul, genre=genre, lokasi=lokasi, status=status, created_by=created_by)
                db.session.add(insertData)
                db.session.commit()
                db.session.close()
                return flash('BERHASIL MENAMBAHKAN BUKU', category="flash-ok")
        else:
            messagebuku = 'KODE BUKU HARUS 6 DIGIT'
            return flash(messagebuku, category="flash-error")

# FUNGSI MENAMBAHKAN DATA KODE RAK
def tambahKodeRak():
    if request.method == 'POST':
        koderakin = request.form['koderak']
        namarakin = request.form['namarak']
        lenkoderak = len(koderakin)
        print(koderakin,namarakin,lenkoderak)
        cekkoderak = koderak.query.filter_by(koderak=koderakin).first()
        messagebuku = ''
        if lenkoderak == 2:
            if not koderakin:
                messagebuku = 'Masukkan Kode Rak'
            elif not namarakin:
                messagebuku = 'Masukkan Nama Rak'
            elif cekkoderak:
                messagebuku = 'Kode Rak Sudah Terpakai'
            
            if not messagebuku:
                insertData = koderak(koderak=koderakin, namarak=namarakin)
                db.session.add(insertData)
                db.session.commit()
                db.session.close()
                return flash('BERHASIL MENAMBAHKAN KODE RAK', category="flash-ok")
        else:
            messagebuku = 'KODE RAK HARUS 2 DIGIT'
            return flash(messagebuku, category="flash-error")

# FUNGSI MENAMBAHKAN DATA KODE RAK
def tambahKodeGenre():
    if request.method == 'POST':
        kodegenrein = request.form['kodegenre']
        namagenrein = request.form['namagenre']
        lenkodegenre = len(kodegenrein)
        cekkodegenre = kodegenre.query.filter_by(kodegenre=kodegenrein).first()
        messagebuku = ''
        if lenkodegenre == 2:
            if not kodegenrein:
                messagebuku = 'Masukkan Kode Genre'
            elif not namagenrein:
                messagebuku = 'Masukkan Nama Genre'
            elif cekkodegenre:
                messagebuku = 'Kode Genre Sudah Terpakai'
            
            if not messagebuku:
                insertData = kodegenre(kodegenre=kodegenrein, namagenre=namagenrein)
                db.session.add(insertData)
                db.session.commit()
                db.session.close()
                return flash('BERHASIL MENAMBAHKAN KODE GENRE', category="flash-ok")
        else:
            messagebuku = 'KODE GENRE HARUS 2 DIGIT'
            return flash(messagebuku, category="flash-error")

# FUNGSI PENCARIAN DATA BUKU
def searchBuku(): 
    ci = cj = cg = cp = ca = ''
    bukusearch = db.session.query(buku.id, buku.kodebuku, buku.judul, buku.genre, buku.lokasi, buku.status).filter(buku.status=="ada", buku.flag=="on").all()
    if request.method == 'POST': 
        carikodebuku  = ci = request.form['carikodebuku']   #Value ci
        carijudul = cj = request.form['carijudul']          #Value cj
        carigenre = cg = request.form['carigenre']          #Value cg
        caripinjam = cp = request.form.get('caripinjam')    #Value cp
        cariada = ca = request.form.get('cariada')          #Value ca

        ci = "%"+str(carikodebuku)+"%"
        cj = "%"+str(carijudul)+"%"
        cg = "%"+str(carigenre)+"%"

        if not cp and not ca:
            bukusearch = db.session.query(buku.id, buku.kodebuku, buku.judul, buku.genre, buku.lokasi, buku.status).filter(buku.kodebuku.like(ci), buku.judul.like(cj), buku.genre.like(cg), buku.flag=="on").all()
        elif not cp and ca:
            bukusearch = db.session.query(buku.id, buku.kodebuku, buku.judul, buku.genre, buku.lokasi, buku.status).filter(buku.kodebuku.like(ci), buku.judul.like(cj), buku.genre.like(cg), buku.status==ca, buku.flag=="on").all()
        elif cp and not ca:
            bukusearch = db.session.query(buku.id, buku.kodebuku, buku.judul, buku.genre, buku.lokasi, buku.status).filter(buku.kodebuku.like(ci), buku.judul.like(cj), buku.genre.like(cg), buku.status==cp, buku.flag=="on").all()
        elif cp and ca:
            bukusearch = db.session.query(buku.id, buku.kodebuku, buku.judul, buku.genre, buku.lokasi, buku.status).filter(buku.kodebuku.like(ci), buku.judul.like(cj), buku.genre.like(cg), buku.flag=="on").all()
    return bukusearch, ci, cj, cg, cp, ca

# FUNGSI MENAMBAHKAN DATA BUKU MENGGUNAKAN CSV
def uploadBuku():
    if request.method == 'POST':
        #Input Form HTML
        filebuku = request.files['filebuku']
        created_by = request.form['created_by']
        updated_by = request.form['updated_by']
        # Definisi Variabel Pendukung
        kodebuku = kodebukuin = judul = genre = lokasi = ''
        statusada = "ada"
        statusdipinjam = "dipinjam"
        flag = "updated"
        strold = "_updated_"+str(time.time())
        skipkosong = skipdigit = 0
        # Proses UPLOAD
        if filebuku.filename != '':
            #set_filename (waktu_upload-nama_file)
            timefilename = datetime.fromtimestamp(time.time()).strftime('%d-%m-%Y_%H.%M.%S..%f_')
            timefilename += filebuku.filename
            #cursor path ke static/files
            filepath = os.path.join(FOLDER_CSVBUKU, timefilename)
            #save file on path static/files
            filebuku.save(filepath)
            #CEK FORMAT
            with open(filepath) as file:
                csv_filebukulen = csv.reader(file)
                length = len(list(csv_filebukulen)[0])
                if length == 4:
                    #CEK PENAMAAN
                    with open(filepath) as file:
                        csv_filebukuhead = csv.reader(file)
                        kodebuku, judul, genre, lokasi = list(csv_filebukuhead)[0]
                        if kodebuku == 'KODE BUKU' and judul == 'JUDUL BUKU' and genre == 'GENRE' and lokasi == 'LOKASI':
                            #PROSES UPLOAD
                            with open(filepath) as file:
                                csv_filebuku = csv.reader(file)
                                next(csv_filebuku)
                                for row in csv_filebuku:
                                    kodebuku, judul, genre, lokasi = list(row)
                                    lenkodebukucsv = len(kodebuku)
                                    if kodebuku and judul and genre and lokasi:
                                        if lenkodebukucsv == 6:
                                            datasama = db.session.query(buku.kodebuku).filter_by(kodebuku=kodebuku).first()
                                            if datasama:
                                                datadipinjam = db.session.query(buku.kodebuku).filter_by(status=statusdipinjam).first()
                                                if datadipinjam:
                                                    kodebukuin = db.session.query(buku.kodebuku).filter_by(kodebuku=kodebuku).first()[0]
                                                    kodebukuold = kodebukuio = str(db.session.query(buku.kodebuku).filter_by(kodebuku=kodebukuin).first()[0])
                                                    kodebukuold += strold
                                                    judulold = str(db.session.query(buku.judul).filter_by(kodebuku=kodebukuin).first()[0])
                                                    genreold = str(db.session.query(buku.genre).filter_by(kodebuku=kodebukuin).first()[0])
                                                    lokasiold = str(db.session.query(buku.lokasi).filter_by(kodebuku=kodebukuin).first()[0])
                                                    
                                                    updateData = buku.query.filter_by(kodebuku=kodebukuin).first()
                                                    updateData.kodebuku = kodebukuold
                                                    updateData.judul = judulold
                                                    updateData.genre = genreold
                                                    updateData.lokasi = lokasiold
                                                    updateData.updated_at = datetime.now()
                                                    updateData.updated_by = updated_by
                                                    updateData.flag = flag
                                                    db.session.commit()

                                                    insertData = buku(kodebuku=kodebukuio, judul=judulold, genre=genreold, lokasi=lokasi, status=statusdipinjam, created_by=created_by)
                                                    db.session.add(insertData)
                                                    db.session.commit()
                                                    db.session.close()

                                                elif not datadipinjam:
                                                    kodebukuin = db.session.query(buku.kodebuku).filter_by(kodebuku=kodebuku).first()[0]
                                                    kodebukuold = kodebukuio = str(db.session.query(buku.kodebuku).filter_by(kodebuku=kodebukuin).first()[0])
                                                    kodebukuold += strold
                                                    judulold = str(db.session.query(buku.judul).filter_by(kodebuku=kodebukuin).first()[0])
                                                    genreold = str(db.session.query(buku.genre).filter_by(kodebuku=kodebukuin).first()[0])
                                                    lokasiold = str(db.session.query(buku.lokasi).filter_by(kodebuku=kodebukuin).first()[0])
                                                    
                                                    updateData = buku.query.filter_by(kodebuku=kodebukuin).first()
                                                    updateData.kodebuku = kodebukuold
                                                    updateData.judul = judulold
                                                    updateData.genre = genreold
                                                    updateData.lokasi = lokasiold
                                                    updateData.updated_at = datetime.now()
                                                    updateData.updated_by = updated_by
                                                    updateData.flag = flag
                                                    db.session.commit()

                                                    insertData = buku(kodebuku=kodebuku, judul=judul, genre=genre, lokasi=lokasi, status=statusada, created_by=created_by)
                                                    db.session.add(insertData)
                                                    db.session.commit()
                                                    db.session.close()

                                            elif not datasama:
                                                insertData = buku(kodebuku=kodebuku, judul=judul, genre=genre, lokasi=lokasi, status=statusada, created_by=created_by)
                                                db.session.add(insertData)
                                                db.session.commit()
                                                db.session.close()
                                        else:
                                            skipdigit = skipdigit + 1
                                    else:
                                        skipkosong = skipkosong + 1
                        else:
                            flash('GAGAL MENGUPLOAD, COBA CEK KEMBALI PENAMAANNYA', category="flash-error")
                            
                else:
                    flash('GAGAL MENGUPLOAD, COBA CEK KEMBALI FORMATNYA', category="flash-error")
    
    flash('BERHASIL MENGUPLOAD DATA BUKU', category="flash-ok")
    if skipkosong == 0 and skipdigit == 0:
        flash('DATA YANG TERSKIP = '+str(skipkosong)+' DATA ADA YANG KOSONG, '+str(skipdigit)+' DATA DENGAN KODE BUKU TIDAK 6 DIGIT', category="flash-ok")
    else:
        flash('DATA YANG TERSKIP = '+str(skipkosong)+' DATA ADA YANG KOSONG, '+str(skipdigit)+' DATA DENGAN KODE BUKU TIDAK 6 DIGIT', category="flash-error")

# FUNGSI MENDAPATKAN DATA BUKU BERDASARKAN ID
def getBuku(id): 
    getbuku = buku.query.filter_by(id=id).first()

    if getbuku is None:
        abort(404, f"buku dengan id {id} tidak ditemukan")

    return getbuku

# FUNGSI MENGEDIT DATA BUKU YANG MASIH TERSEDIA
def updateBukuAda(id): 
    getbuku = getBuku(id)
    kodebukuold = str(db.session.query(buku.kodebuku).filter_by(id=id).first()[0])
    judulold = str(db.session.query(buku.judul).filter_by(id=id).first()[0])
    genreold = str(db.session.query(buku.genre).filter_by(id=id).first()[0])
    lokasiold = str(db.session.query(buku.lokasi).filter_by(id=id).first()[0])
    strold = "_updated_"+str(time.time())
    kodebukuold += strold
    
    if request.method == 'POST':
        kodebuku = request.form['kodebuku']
        judul = request.form['judul']
        genre = request.form['genre']
        lokasi = request.form['lokasi']
        status = request.form['status']
        flag = request.form['flag']
        created_by = request.form['created_by']
        updated_by = request.form['updated_by']
        messagebuku = ''
        if not kodebuku:
            messagebuku = 'Masukkan Kode Buku'
        elif not judul:
            messagebuku = 'Masukkan Judul Buku'
        elif not genre:
            messagebuku = 'Masukkan Genre Buku'
        elif not lokasi:
            messagebuku = 'Tulis Lokasi Rak Buku'
            
        if not messagebuku:
            updateData = buku.query.filter_by(id=id).first()
            updateData.kodebuku = kodebukuold
            updateData.judul = judulold
            updateData.genre = genreold
            updateData.lokasi = lokasiold
            updateData.updated_at = datetime.now()
            updateData.updated_by = updated_by
            updateData.flag = flag
            db.session.commit()
            insertData = buku(kodebuku=kodebuku, judul=judul, genre=genre, lokasi=lokasi, status=status, created_by=created_by)
            db.session.add(insertData)
            db.session.commit()
            db.session.close()
            flash('BERHASIL MENGEDIT DATA BUKU', category="flash-ok")
            renderself = False
            return renderself, getbuku
        else:
            flash(messagebuku, category="flash-error")
            renderself = True
            return renderself, getbuku
    else:
        renderself = True
        return renderself, getbuku

# FUNGSI MENGEDIT DATA BUKU YANG DIPINJAM
def updateBukuDipinjam(id): 
    getbuku = getBuku(id)
    kodebukuold = str(db.session.query(buku.kodebuku).filter_by(id=id).first()[0])
    judulold = str(db.session.query(buku.judul).filter_by(id=id).first()[0])
    genreold = str(db.session.query(buku.genre).filter_by(id=id).first()[0])
    lokasiold = str(db.session.query(buku.lokasi).filter_by(id=id).first()[0])
    strold = "_updated_"+str(time.time())
    kodebukuold += strold
    if request.method == 'POST':
        kodebuku = request.form['kodebuku']
        judul = request.form['judul']
        genre = request.form['genre']
        lokasi = request.form['lokasi']
        status = request.form['status']
        flag = request.form['flag']
        created_by = request.form['created_by']
        updated_by = request.form['updated_by']
        messagebuku = ''

        if not kodebuku:
            messagebuku = 'Masukkan Kode Buku'
        elif not judul:
            messagebuku = 'Masukkan Judul Buku'
        elif not genre:
            messagebuku = 'Masukkan Genre Buku'
        elif not lokasi:
            messagebuku = 'Tulis Lokasi Rak Buku'
            
        if not messagebuku:
            updateData = buku.query.filter_by(id=id).first()
            updateData.kodebuku = kodebukuold
            updateData.judul = judulold
            updateData.genre = genreold
            updateData.lokasi = lokasiold
            updateData.updated_at = datetime.now()
            updateData.updated_by = updated_by
            updateData.flag = flag
            db.session.commit()
            insertData = buku(kodebuku=kodebuku, judul=judul, genre=genre, lokasi=lokasi, status=status, created_by=created_by)
            db.session.add(insertData)
            db.session.commit()
            db.session.close()
            flash('BERHASIL MENGEDIT DATA BUKU', category="flash-ok")
            renderself = False
            return renderself, getbuku

        else:
            flash(messagebuku, category="flash-error")
            renderself = True
            return renderself, getbuku
    else:
        renderself = True
        return renderself, getbuku
        
# FUNGSI MENGHAPUS DATA BUKU
def deleteBuku(id): 
    getBuku(id)
    delstr = "_deleted_"+str(time.time())
    kodebuku = str(db.session.query(buku.kodebuku).filter_by(id=id).first()[0])
    kodebuku += delstr
    if request.method == 'POST':
        updated_by = request.form['updated_by']
        updateData = buku.query.filter_by(id=id).first()
        updateData.kodebuku = kodebuku
        updateData.updated_at = datetime.now()
        updateData.updated_by = updated_by
        updateData.flag = "deleted"
        db.session.commit()
        db.session.close()
        flash('Berhasil Menghapus Data Buku', category="flash-ok")

# FUNGSI MENDOWNLOAD / MENGKEXPORT DATA BUKU DENGAN FORMAT CSV
def downloadBuku():
    ci = cj = cg = cp = ca = ''
    bukucsv = db.session.query(buku.kodebuku, buku.judul, buku.genre, buku.lokasi, buku.status).filter_by(status='ada', flag='on').all()
    if request.method == 'POST':
        carikodebuku  = ci = request.form['ci']
        carijudul = cj = request.form['cj']
        carigenre = cg = request.form['cg']
        caripinjam = cp = request.form.get('cp')
        cariada = ca = request.form.get('ca')

        if cp == 'None' and ca == 'None':
            cp = ca = ''
        elif cp == 'None' and ca == 'ada':
            cp = ''
        elif cp == 'dipinjam' and ca == 'None':
            ca = ''

        ci = "%"+str(carikodebuku)+"%"
        ci = "%"+str(carijudul)+"%"
        ci = "%"+str(carigenre)+"%"

        if not cp and not ca:
            bukucsv = db.session.query(buku.kodebuku, buku.judul, buku.genre, buku.lokasi, buku.status).filter(buku.kodebuku.like(ci), buku.judul.like(cj), buku.genre.like(cg), buku.flag=="on").all()
        elif not cp and ca:
            bukucsv = db.session.query(buku.kodebuku, buku.judul, buku.genre, buku.lokasi, buku.status).filter(buku.kodebuku.like(ci), buku.judul.like(cj), buku.genre.like(cg), buku.status==ca, buku.flag=="on").all()
        elif cp and not ca:
            bukucsv = db.session.query(buku.kodebuku, buku.judul, buku.genre, buku.lokasi, buku.status).filter(buku.kodebuku.like(ci), buku.judul.like(cj), buku.genre.like(cg), buku.status==cp, buku.flag=="on").all()
        elif cp and ca:
            bukucsv = db.session.query(buku.kodebuku, buku.judul, buku.genre, buku.lokasi, buku.status).filter(buku.kodebuku.like(ci), buku.judul.like(cj), buku.genre.like(cg), buku.flag=="on").all()

    export_buku = ['KODE BUKU', 'JUDUL BUKU', 'GENRE', 'LOKASI', 'STATUS BUKU']
    si = StringIO()
    cw = csv.writer(si)
    cw.writerow(export_buku)
    cw.writerows(bukucsv)
    output = make_response(si.getvalue())
    output.headers["Content-Disposition"] = "attachment; filename=databuku.csv"
    output.headers["Content-type"] = "text/csv"
    return output

# FUNGSI MENDOWNLOAD FORMAT UPLOAD BUKU MENGGUNAKAN CSV
def downloadFormatBuku():
    if request.method == 'POST':
        carikodebuku  = ci = request.form['ci']
        ci = "%"+str(carikodebuku)+"%"

    export_buku = ['KODE BUKU', 'JUDUL BUKU', 'GENRE', 'LOKASI']
    si = StringIO()
    cw = csv.writer(si)
    cw.writerow(export_buku)
    cw.writerows(db.session.query(buku).filter(buku.kodebuku.like(ci), buku.flag=="on").all())
    output = make_response(si.getvalue())
    output.headers["Content-Disposition"] = "attachment; filename=databuku.csv"
    output.headers["Content-type"] = "text/csv"
    return output