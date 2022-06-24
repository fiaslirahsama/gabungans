from flask_sqlalchemy import SQLAlchemy
from app_hospital import db
from app_hospital.dokter.model_dokter import dokter

# This file work for define and initialize model for the database.

class dokter_history(db.Model):
    no_dokter_history = db.Column(db.Integer, primary_key=True, autoincrement=True)
    id_dokter = db.Column(db.Integer, db.ForeignKey('dokter.id_dokter'))
    username = db.Column(db.String(99), nullable=False)
    nama_dokter = db.Column(db.String(80), nullable=False)
    hari_kerja = db.Column(db.String(80), nullable=False)
    jam_kerja = db.Column(db.String(80), nullable=False)
    kuota = db.Column(db.Integer, nullable=False)
    flag = db.Column(db.String(2), nullable=False)
    created_date = db.Column(db.DateTime, nullable=False)

    def __init__(self, id_dokter, kuota, username, nama_dokter, hari_kerja, jam_kerja, flag, created_date):
        self.id_dokter = id_dokter
        self.username = username
        self.nama_dokter = nama_dokter
        self.hari_kerja = hari_kerja
        self.jam_kerja = jam_kerja
        self.kuota = kuota
        self.flag = flag
        self.created_date = created_date
    
    def __repr__(self):
        return '<dokter_history %r>' % self.no_dokter_history