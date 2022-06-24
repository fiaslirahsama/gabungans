from flask import *
from app_hospital.dokter.model_dokter import dokter
from app_hospital.auth.model_auth import auth
from app_hospital.auth import controller_auth
from app_hospital.dokter_history import controller_dokter_history
from app_hospital import db, generate_password_hash, pd, BytesIO
import datetime

def viewDokter():
    try:
        view = dokter.query.filter(dokter.flag=="Y").all()
        return view
    except Exception as e:
        return flash(e)

def searchDokter():
    try:
        id_dokter = request.form.get('id_dokter')
        nama_dokter = request.form.get('nama_dokter')
        hari_kerja = request.form.get('hari_kerja')
        jam_kerja = request.form.get('jam_kerja')
        if id_dokter == '': 
            id_dokter = '%'
        else:
            id_dokter = id_dokter
        if nama_dokter == '':
            nama_dokter = '%'
        else:
            nama_dokter = '%'+nama_dokter+'%'
        if hari_kerja == '':
            hari_kerja = '%'
        else:
            hari_kerja = '%'+hari_kerja+'%'
        if jam_kerja == '':
            jam_kerja = '%'
        else:
            jam_kerja = '%'+jam_kerja+'%'
        search = dokter.query.filter(dokter.flag=='Y', dokter.id_dokter.like(id_dokter), dokter.nama_dokter.like(nama_dokter), dokter.hari_kerja.like(hari_kerja), dokter.jam_kerja.like(jam_kerja)).all()
        return search
    except Exception as e:
        return flash(e)

def addDokter():
    try:
        status_auth = 'dokter'
        username = request.form.get('username')
        password = request.form.get('password')
        nama_dokter = request.form.get('nama_dokter')
        hari_kerja = request.form.get('hari_kerja')
        jam_kerja = request.form.get('jam_kerja')
        date = datetime.datetime.now()
        newUser = auth(username=username, status_auth=status_auth, password=generate_password_hash(password, method='sha256'), flag="Y", created_date=date, updated_date=date)
        db.session.add(newUser)
        db.session.commit()
        id_auth = controller_auth.findIdAuth(username)
        saveDokter = dokter(id_auth=id_auth, username=username, password=password, nama_dokter=nama_dokter, hari_kerja=hari_kerja, jam_kerja=jam_kerja, status_pemeriksaan='N', flag="Y", kuota=5, created_date=date, updated_date=date)
        db.session.add(saveDokter)
        db.session.commit()
        db.session.close()
        return flash("Data Dokter Berhasil Ditambahkan.")
    except Exception as e:
        return flash(e)

def editDokter(id_dokter):
    id_dokter = request.form.get('id_dokter1')
    username = request.form.get('username1')
    password = request.form.get('password1')
    nama_dokter = request.form.get('nama_dokter1')
    hari_kerja = request.form.get('hari_kerja1')
    jam_kerja = request.form.get('jam_kerja1')
    kuota = request.form.get('kuota1')
    edit = dokter.query.filter(dokter.id_dokter==id_dokter, dokter.flag=='Y').first()
    controller_dokter_history.addDokterHistory(edit.id_dokter, edit.username, edit.nama_dokter, edit.hari_kerja, edit.jam_kerja, edit.kuota)
    edit.username = username
    edit.password = password
    edit.nama_dokter = nama_dokter
    edit.hari_kerja = hari_kerja
    edit.jam_kerja = jam_kerja
    edit.kuota = kuota
    edit.updated_date = datetime.datetime.now()
    edit.flag = 'Y'
    db.session.commit()
    saveAuth = auth.query.filter(auth.id_auth==edit.id_auth)
    saveAuth.username = username
    saveAuth.password = generate_password_hash(password, method='sha256')
    db.session.commit()
    db.session.close()
    return flash("Data Dokter Behasil di Update.")

def deleteDokter(id_dokter):
    try:
        delete = dokter.query.filter(dokter.id_dokter==id_dokter).first()
        delete.flag = "N"
        delete.updated_date = datetime.datetime.now()
        db.session.commit()
        saveAuth = auth.query.filter(auth.username==delete.username).first()
        saveAuth.flag = "N"
        db.session.commit()
        db.session.close()
        return flash("Data Dokter Berhasil di Hapus.")
    except Exception as e:
        return flash(e)

def findDokterWithId(id_dokter):
    try:
        rows = dokter.query.filter(dokter.id_dokter==id_dokter, dokter.flag=='Y').first()
        return rows.kuota
    except Exception as e:
        return flash(e)
    
def downloadTemplateDokter():
    df_1 = pd.DataFrame(columns=['Nama Dokter', 'Hari Kerja', 'Jam Kerja', 'Username', 'Password',])
    output = BytesIO()
    writer = pd.ExcelWriter(output, engine='xlsxwriter')
    df_1.to_excel(writer, sheet_name = "Sheet_1")
    workbook = writer.book
    worksheet = writer.sheets["Sheet_1"]
    format = workbook.add_format()
    format.set_bg_color('#eeeeee')
    worksheet.set_column(0,2)
    writer.close()
    output.seek(0)
    return send_file(output, attachment_filename="Template_Dokter.xlsx", as_attachment=True)

def importAddDokter():
    f = request.files['file']
    data_xls = pd.read_excel(f)
    created_date = datetime.datetime.now()
    updated_date = datetime.datetime.now()
    for i in range(len(data_xls)):
        nama_dokter = data_xls.loc[i][1]
        hari_kerja = data_xls.loc[i][2]
        jam_kerja = data_xls.loc[i][3]
        username = data_xls.loc[i][4]
        password = data_xls.loc[i][5]
        newUser = auth(username=username, status_auth='dokter', password=generate_password_hash(password, method='sha256'), flag="Y", created_date=created_date, updated_date=updated_date)
        db.session.add(newUser)
        db.session.commit()
        id = controller_auth.findIdAuth(username)
        saveAdd = dokter(id_auth=id, kuota=5, username=username, password=password, nama_dokter=nama_dokter, hari_kerja=hari_kerja, jam_kerja=jam_kerja, flag="Y", status_pemeriksaan='N', created_date=created_date, updated_date=updated_date)
        db.session.add(saveAdd)
        db.session.commit()
    db.session.close()
    return flash("Data Berhasil Ditambahkan.")