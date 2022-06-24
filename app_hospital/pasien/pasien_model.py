from flask_sqlalchemy import SQLAlchemy
from app_hospital import db

# This file work for define and initialize model for the database.

class pasien(db.Model):
    no_pasien = db.Column(db.Integer, primary_key=True, autoincrement=True)
    nama_pasien = db.Column(db.String(80), nullable=False)
    alamat_pasien = db.Column(db.String(80), nullable=False)
    status_diperiksa = db.Column(db.String(2), nullable=False)
    flag = db.Column(db.String(2), nullable=False)
    created_date = db.Column(db.DateTime, nullable=False)
    updated_date = db.Column(db.DateTime, nullable=False)

    def __init__(self, nama_pasien, status_diperiksa, alamat_pasien, flag, created_date, updated_date):
        self.nama_pasien = nama_pasien
        self.alamat_pasien = alamat_pasien
        self.status_diperiksa = status_diperiksa
        self.flag = flag
        self.created_date = created_date
        self.updated_date = updated_date
    
    def __repr__(self):
        return '<pasien %r>' % self.no_pasien