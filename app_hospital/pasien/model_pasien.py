from flask_sqlalchemy import SQLAlchemy
from app_hospital import db
from app_hospital.auth.model_auth import auth

# This file work for define and initialize model for the database.

class pasien(db.Model):
    no_pasien = db.Column(db.Integer, primary_key=True, autoincrement=True)
    id_auth = db.Column(db.Integer, db.ForeignKey('auth.id_auth'))
    username = db.Column(db.String(99), nullable=False)
    password = db.Column(db.String(99), nullable=False)
    nama_pasien = db.Column(db.String(80), nullable=False)
    alamat_pasien = db.Column(db.String(80), nullable=False)
    status_diperiksa = db.Column(db.String(2), nullable=False)
    flag = db.Column(db.String(2), nullable=False)
    created_date = db.Column(db.DateTime, nullable=False)
    updated_date = db.Column(db.DateTime, nullable=False)

    def __init__(self, id_auth, nama_pasien, username, password, status_diperiksa, alamat_pasien, flag, created_date, updated_date):
        self.id_auth = id_auth
        self.nama_pasien = nama_pasien
        self.username = username
        self.password = password
        self.alamat_pasien = alamat_pasien
        self.status_diperiksa = status_diperiksa
        self.flag = flag
        self.created_date = created_date
        self.updated_date = updated_date
    
    def __repr__(self):
        return '<pasien %r>' % self.no_pasien