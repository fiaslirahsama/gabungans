from flask_sqlalchemy import SQLAlchemy
from app_hospital import db

# This file work for define and initialize model for the database.

class dokter_history(db.Model):
    no_dokter_history = db.Column(db.Integer, primary_key=True, autoincrement=True)
    id_dokter = db.Column(db.Integer, db.ForeignKey('dokter.id_dokter'), nullable=False)
    nama_dokter = db.Column(db.String(80), nullable=False)
    hari_kerja = db.Column(db.String(80), nullable=False)
    jam_kerja = db.Column(db.String(80), nullable=False)
    status_pemeriksaan = db.Column(db.String(2), nullable=False)
    flag = db.Column(db.String(2), nullable=False)
    created_date = db.Column(db.DateTime, nullable=False)

    def __init__(self, id_dokter, nama_dokter, hari_kerja, jam_kerja, status_pemeriksaan, flag, created_date):
        self.id_dokter = id_dokter
        self.nama_dokter = nama_dokter
        self.hari_kerja = hari_kerja
        self.jam_kerja = jam_kerja
        self.status_pemeriksaan = status_pemeriksaan
        self.flag = flag
        self.created_date = created_date
    
    def __repr__(self):
        return '<dokter_history %r>' % self.no_dokter_history