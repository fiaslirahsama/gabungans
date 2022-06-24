from flask_sqlalchemy import SQLAlchemy
from app_hospital import db

# This file work for define and initialize model for the database.

class dokter(db.Model):
    id_dokter = db.Column(db.Integer, primary_key=True, autoincrement=True)
    nama_dokter = db.Column(db.String(80), nullable=False)
    hari_kerja = db.Column(db.String(80), nullable=False)
    jam_kerja = db.Column(db.String(80), nullable=False)
    status_pemeriksaan = db.Column(db.String(2), nullable=False)
    flag = db.Column(db.String(2), nullable=False)
    created_date = db.Column(db.DateTime, nullable=False)
    updated_date = db.Column(db.DateTime, nullable=False)

    def __init__(self, nama_dokter, hari_kerja, jam_kerja, status_pemeriksaan, flag, created_date, updated_date):
        self.nama_dokter = nama_dokter
        self.hari_kerja = hari_kerja
        self.jam_kerja = jam_kerja
        self.status_pemeriksaan = status_pemeriksaan
        self.flag = flag
        self.created_date = created_date
        self.updated_date = updated_date
    
    def __repr__(self):
        return '<dokter %r>' % self.id_dokter