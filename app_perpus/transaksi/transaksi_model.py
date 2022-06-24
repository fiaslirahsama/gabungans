# Berisi pemodelan tabel data pada database
from datetime import datetime, timedelta
from flask_sqlalchemy import SQLAlchemy
from app_perpus import db

def waktu_sekarang():
    now = datetime.now()
    return now
def hari_sekarang():
    datenow = datetime.now().date()
    return datenow

class transaksi(db.Model):
    id = db.Column(db.Integer, index=True, primary_key=True, autoincrement=True)
    idmember = db.Column(db.String(6), db.ForeignKey('member.idmember'), nullable=False)
    kodebuku = db.Column(db.String(6), db.ForeignKey('buku.kodebuku'), nullable=False)
    tgl_pinjam = db.Column(db.Date, nullable=False, default=hari_sekarang)
    tgl_kembali = db.Column(db.Date, nullable=False)
    idadmin = db.Column(db.Integer, db.ForeignKey('admin_perpus.id'), nullable=False)
    created_at = db.Column(db.DateTime, nullable=False, default=waktu_sekarang)
    created_by = db.Column(db.String(30), nullable=False)
    updated_at = db.Column(db.DateTime, nullable=True)
    updated_by = db.Column(db.String(30), nullable=True)
    flag = db.Column(db.String(10), nullable=False, default='on')
     
    def __init__(self, idmember, kodebuku, tgl_kembali, idadmin, created_by):
        self.idmember = idmember
        self.kodebuku = kodebuku
        self.tgl_kembali= tgl_kembali
        self.idadmin = idadmin
        self.created_by = created_by

    def __repr__(self):
        return '<buku %r>' % self.id

    def get_id(self):
        return str(self.id)