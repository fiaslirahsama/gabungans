from flask_sqlalchemy import SQLAlchemy
from app_hospital import db
from app_hospital.auth.model_auth import auth

# This file work for define and initialize model for the database.

class dokter(db.Model):
    id_dokter = db.Column(db.Integer, primary_key=True, autoincrement=True)
    id_auth = db.Column(db.Integer, db.ForeignKey('auth.id_auth'))
    username = db.Column(db.String(99), nullable=False)
    password = db.Column(db.String(99), nullable=False)
    nama_dokter = db.Column(db.String(80), nullable=False)
    hari_kerja = db.Column(db.String(80), nullable=False)
    jam_kerja = db.Column(db.String(80), nullable=False)
    status_pemeriksaan = db.Column(db.String(2), nullable=False)
    kuota = db.Column(db.Integer, nullable=False)
    flag = db.Column(db.String(2), nullable=False)
    created_date = db.Column(db.DateTime, nullable=False)
    updated_date = db.Column(db.DateTime, nullable=False)

    def __init__(self, kuota, id_auth, status_pemeriksaan, nama_dokter, username, password, hari_kerja, jam_kerja, flag, created_date, updated_date):
        self.id_auth = id_auth
        self.kuota = kuota
        self.nama_dokter = nama_dokter
        self.username = username
        self.password = password
        self.hari_kerja = hari_kerja
        self.jam_kerja = jam_kerja
        self.flag = flag
        self.created_date = created_date
        self.updated_date = updated_date
        self.status_pemeriksaan = status_pemeriksaan
    
    def __repr__(self):
        return '<dokter %r>' % self.id_dokter