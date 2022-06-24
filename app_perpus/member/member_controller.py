# Berisi fungsi-fungsi untuk menjalankan program member
from flask import(
    Blueprint, flash, g, redirect, render_template, request, url_for, make_response
)
import os, csv, time
from os.path import join, dirname, realpath
from werkzeug.exceptions import abort
from io import StringIO
from app_perpus import db
from app_perpus.member.member_model import member
from datetime import datetime, timedelta

# Mendefinisikan folder untuk menyimpan file csv member
BASEDIR = os.path.abspath(os.path.dirname(os.path.dirname(realpath(__file__))))
FOLDER_CSVMEMBER = os.path.join(BASEDIR, './static/csvupload/member/')

# FUNGSI GENERATE 6 DIGIT ANGKA RANDOM UNTUK ID MEMBER
# def random():
#     import random, math
#     digits = [i for i in range(0,10)]
#     random_str = ""
#     for i in range(6):
#         index = math.floor(random.random()*10)
#         random_str += str(digits[index])
#     return random_str
def generateIdMember():
    idmember = db.session.query(member.idmember).filter_by(idmember=100001).first()
    if idmember:
        datamember = db.session.query(member.idmember).all()
        increment = len(datamember)
        for idmem in idmember:
            idmember = int(idmem) + increment
        return idmember
    else:
        idmember = 100001
        return idmember

# FUNGSI MENAMPILKAN DATA MEMBER
def dataMember():
    generateid = generateIdMember()
    while True:
        cekid = db.session.query(member.idmember).filter_by(idmember=generateid).first()
        if cekid:
            generateid = generateid + 1
            continue
        else:
            break

    return generateid

# FUNGSI MENAMBAHKAN DATA MEMBER
def tambahMember():
    if request.method == 'POST':
        if 'tambahmember' in request.form:
            idmember = request.form['idmember']
            nik = request.form['nik']
            nama = request.form['nama']
            jenis_kelamin = request.form['jenis_kelamin']
            alamat = request.form['alamat']
            created_by = request.form['created_by']
            lenidmember = len(idmember)
            cekmember = db.session.query(member.idmember).filter_by(idmember=idmember).first()
            messagemember = ''
            if lenidmember == 6:
                if not idmember:
                    messagemember = 'Masukkan ID Member'
                elif not nik:
                    messagemember = 'Masukkan NIK'
                elif not nama:
                    messagemember = 'Masukkan Nama'
                elif not jenis_kelamin:
                    messagemember = 'Masukkan Jenis Kelamin'
                elif not alamat:
                    messagemember = 'Masukkan Alamat'
                elif cekmember:
                    messagemember = 'ID Member Sudah Terpakai'
                
                if not messagemember:
                    insertData = member(idmember=idmember, nik=nik, nama=nama, jenis_kelamin=jenis_kelamin, alamat=alamat, created_by=created_by) 
                    db.session.add(insertData)
                    db.session.commit()
                    db.session.close()
                    flash("Data Member Berhasil Disimpan", category="flash-ok")
            else:
                messagemember = 'ID MEMBER HARUS 6 DIGIT'
                flash(messagemember, category="flash-error")

# FUNGSI PENCARIAN DATA MEMBER
def searchMember():
    ci = cni = cna = cj = ca = ''
    membersearch = []
    membersearch = db.session.query(member.id, member.idmember, member.nik, member.nama, member.jenis_kelamin, member.alamat).filter(member.flag=="on").all()
    if request.method == 'POST':
        if 'caridatamember' in request.form:
            cariidmember  = ci = request.form['cariidmember']
            carinik = cni = request.form['carinik']
            carinama = cna = request.form['carinama']
            carijenis = cj = request.form.get('carijenis')
            carialamat = ca = request.form.get('carialamat')

            ci = cni = cna = cj = ca = p = "%"
            ci += str(cariidmember)
            ci += p
            cni += str(carinik)
            cni += p
            cna += str(carinama)
            cna += p
            cj += str(carijenis)
            cj += p
            ca += str(carialamat)
            ca += p
            membersearch = db.session.query(member.id, member.idmember, member.nik, member.nama, member.jenis_kelamin, member.alamat).filter(member.idmember.like(ci), member.nik.like(cni), member.nama.like(cna), member.jenis_kelamin.like(cj), member.alamat.like(ca), member.flag=="on").all()
    return membersearch, ci, cni, cna, cj, ca            

# FUNGSI MENDOWNLOAD/EXPORT DATA MEMBER DALAM BENTUK CSV
def downloadMember():
    ci = cni = cna = cj = ca = ''
    membercsv = db.session.query(member.idmember, member.nik, member.nama, member.jenis_kelamin, member.alamat).filter_by(flag='on').all()

    if request.method == 'POST':

        cariidmember  = ci = request.form['ci']
        carinik = cni = request.form['cni']
        carinama = cna = request.form['cna']
        carijenis = cj = request.form.get('cj')
        carialamat = ca = request.form.get('ca')
        ci = cni = cna = cj = ca = p = "%"
        ci += str(cariidmember)
        ci += p
        cni += str(carinik)
        cni += p
        cna += str(carinama)
        cna += p
        cj += str(carijenis)
        cj += p
        ca += str(carialamat)
        ca += p
        membercsv = db.session.query(member.idmember, member.nik, member.nama, member.jenis_kelamin, member.alamat).filter(member.idmember.like(ci), member.nik.like(cni), member.nama.like(cna), member.jenis_kelamin.like(cj), member.alamat.like(ca), member.flag=="on").all()

    export_member = ['ID MEMBER', 'NO TANDA PENGENAL', 'NAMA MEMBER', 'JENIS KELAMIN', 'ALAMAT']
    si = StringIO()
    cw = csv.writer(si)
    cw.writerow(export_member)
    cw.writerows(membercsv)
    output = make_response(si.getvalue())
    output.headers["Content-Disposition"] = "attachment; filename=datamember.csv"
    output.headers["Content-type"] = "text/csv"
    return output

#FUNGSI DOWNLOAD FORMAT UPLOAD CSV DATA MEMBER
def downloadFormatMember():
    if request.method == 'POST':
        cariidmember  = ci = request.form['ci']
        ci = "%"+str(cariidmember)+"%"

    export_member = ['NO TANDA PENGENAL', 'NAMA MEMBER', 'JENIS KELAMIN', 'ALAMAT']
    si = StringIO()
    cw = csv.writer(si)
    cw.writerow(export_member)
    cw.writerows(db.session.query(member.idmember, member.nik, member.nama, member.jenis_kelamin, member.alamat).filter(member.idmember.like(ci), member.flag=="on").all())
    output = make_response(si.getvalue())
    output.headers["Content-Disposition"] = "attachment; filename=datamember.csv"
    output.headers["Content-type"] = "text/csv"
    return output

# FUNGSI MENAMBAHKAN DATA MEMBER MENGGUNAKAN CSV
def uploadMember():
    if request.method == 'POST':
        #Input Form HTML
        filemember = request.files['filemember']
        created_by = request.form['created_by']
        updated_by = request.form['updated_by']
        # Definisi Variabel Pendukung
        idmember = idmemberin = nik = nama = jenis_kelamin = alamat = ''
        flag = "updated"
        strold = "_updated_"+str(time.time())
        skipkosong = skipdigit = 0
        # Proses Upload
        if filemember.filename != '':
            #set filename (Waktu upload_nama file)
            timefilename = datetime.fromtimestamp(time.time()).strftime('%d-%m-%Y_%H.%M.%S..%f_')
            timefilename += filemember.filename
            #cursor path ke static/files
            filepath = os.path.join(FOLDER_CSVMEMBER, timefilename)
            #save file on path static/files
            filemember.save(filepath)
            #CEK FORMAT
            with open(filepath) as file:
                csv_filememberlen = csv.reader(file)
                length = len(list(csv_filememberlen)[0])
                if length == 4:
                    #CEK PENAMAAN
                    with open(filepath) as file:
                        csv_filememberhead = csv.reader(file)
                        nik, nama, jenis_kelamin, alamat = list(csv_filememberhead)[0]
                        if nik == 'NO TANDA PENGENAL' and nama == 'NAMA MEMBER' and jenis_kelamin == 'JENIS KELAMIN' and alamat == 'ALAMAT':
                            #PROSES UPLOAD
                            with open(filepath) as file:
                                csv_filemember = csv.reader(file)
                                next(csv_filemember)
                                for row in csv_filemember:
                                    idmember = str(generateIdMember())
                                    nik, nama, jenis_kelamin, alamat = list(row)
                                    lenidmembercsv = len(idmember)
                                    if idmember and nik and nama and jenis_kelamin and alamat:
                                        if lenidmembercsv == 6:
                                            datasama = db.session.query(member.idmember).filter_by(idmember=idmember).first()
                                            if datasama:
                                                idmemberin = db.session.query(member.idmember).filter_by(idmember=idmember).first()[0]
                                                idmemberold = str(db.session.query(member.idmember).filter_by(idmember=idmemberin).first()[0])
                                                idmemberold += strold
                                                nikold = str(db.session.query(member.nik).filter_by(idmember=idmemberin).first()[0])
                                                namaold = str(db.session.query(member.nama).filter_by(idmember=idmemberin).first()[0])
                                                jenis_kelaminold = str(db.session.query(member.jenis_kelamin).filter_by(idmember=idmemberin).first()[0])
                                                alamatold = str(db.session.query(member.alamat).filter_by(idmember=idmemberin).first()[0])

                                                updateData = member.query.filter_by(idmember=idmemberin).first()
                                                updateData.idmember = idmemberold
                                                updateData.nik = nikold
                                                updateData.nama = namaold
                                                updateData.jenis_kelamin = jenis_kelaminold
                                                updateData.alamat = alamatold
                                                updateData.updated_at = datetime.now()
                                                updateData.updated_by = updated_by
                                                updateData.flag = flag
                                                db.session.commit()
                                                
                                                insertData = member(idmember=idmember, nik=nik, nama=nama, jenis_kelamin=jenis_kelamin, alamat=alamat, created_by=created_by)
                                                db.session.add(insertData)
                                                db.session.commit()
                                                db.session.close()
                                            elif not datasama:
                                                insertData = member(idmember=idmember, nik=nik, nama=nama, jenis_kelamin=jenis_kelamin, alamat=alamat, created_by=created_by)
                                                db.session.add(insertData)
                                                db.session.commit()
                                                db.session.close()
                                        else:
                                            skipdigit = skipdigit + 1
                                    else:
                                        skipkosong = skipkosong + 1
                        else:
                            return flash('GAGAL MENGUPLOAD COBA CEK KEMBALI PENAMAANNYA', category="flash-error")
                else:
                    return flash('GAGAL MENGUPLOAD COBA CEK KEMBALI FORMATNYA', category="flash-error")
                    
    if skipkosong == 0 and skipdigit == 0:
        flash('BERHASIL MENGUPLOAD DATA', category="flash-ok")
        flash('DATA YANG TERSKIP = '+str(skipkosong)+' DATA ADA YANG KOSONG, '+str(skipdigit)+' DATA DENGAN ID MEMBER TIDAK 6 DIGIT', category="flash-ok")
    else:
        flash('DATA YANG TERSKIP = '+str(skipkosong)+' DATA ADA YANG KOSONG, '+str(skipdigit)+' DATA DENGAN ID MEMBER TIDAK 6 DIGIT', category="flash-error")
            
# FUNGSI MENDAPATKAN DATA MEMBER BERDASARKAN ID            
def getMember(id): 
    getmember = member.query.filter_by(id=id).first()

    if not getmember:
        abort(404, f"Member dengan id {id} tidak ditemukan")

    return getmember

# FUNGSI MENGEDIT DATA MEMBER
def updateMember(id): 
    getmember = getMember(id)
    idmemberold = str(db.session.query(member.idmember).filter_by(id=id).first()[0])
    nikold = str(db.session.query(member.nik).filter_by(id=id).first()[0])
    namaold = str(db.session.query(member.nama).filter_by(id=id).first()[0])
    jenis_kelaminold = str(db.session.query(member.jenis_kelamin).filter_by(id=id).first()[0])
    alamatold = str(db.session.query(member.alamat).filter_by(id=id).first()[0])
    strold = "_updated_"+str(time.time())
    idmemberold += strold
    if request.method == 'POST':
        idmember = request.form['idmember']
        nik = request.form['nik']
        nama = request.form['nama']
        jenis_kelamin = request.form['jenis_kelamin']
        alamat = request.form['alamat']
        flag = request.form['flag']
        created_by = request.form['created_by']
        updated_by = request.form['updated_by']
        messagemember = ''

        if not idmember:
            messagemember = 'Masukkan ID Member'
        elif not nik:
            messagemember = 'Masukkan NIK'
        elif not nama:
            messagemember = 'Masukkan Nama'
        elif not jenis_kelamin:
            messagemember = 'Masukkan Jenis Kelamin'
        elif not alamat:
            messagemember = 'Masukkan Alamat'
            
        if not messagemember:
            updateData = member.query.filter_by(id=id).first()
            updateData.idmember = idmemberold
            updateData.nik = nikold
            updateData.nama = namaold
            updateData.jenis_kelamin = jenis_kelaminold
            updateData.alamat = alamatold
            updateData.updated_at = datetime.now()
            updateData.updated_by = updated_by
            updateData.flag = flag
            db.session.commit()
            insertData = member(idmember=idmember, nik=nik, nama=nama, jenis_kelamin=jenis_kelamin, alamat=alamat, created_by=created_by)
            db.session.add(insertData)
            db.session.commit()
            db.session.close()
            flash('Berhasil Mengedit Data Member', category="flash-ok")
            renderself = False
            return renderself, getmember
        else:
            flash(messagemember, category="flash-error")
            renderself = True
            return renderself, getmember
    else:
        renderself = True
        return renderself, getmember
        


# FUNGSI UNTUK MENGHAPUS DATA MEMBER
def deleteMember(id): 
    getMember(id)
    delstr = "_deleted_"+str(time.time())
    idmember = str(db.session.query(member.idmember).filter_by(id=id).first()[0])
    idmember += delstr
    if request.method == 'POST':
        updated_by = request.form['updated_by']
        updateData = member.query.filter_by(id=id).first()
        updateData.idmember = idmember
        updateData.updated_at = datetime.now()
        updateData.updated_by = updated_by
        updateData.flag = "deleted"
        db.session.commit()
        db.session.close()
        flash('Berhasil Menghapus Data Member', category="flash-ok")