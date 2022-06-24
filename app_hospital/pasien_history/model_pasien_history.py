from flask_sqlalchemy import SQLAlchemy
from app_hospital.pasien.model_pasien import pasien
from app_hospital import db

# This file work for define and initialize model for the database.

class pasien_history(db.Model):
    no_pasien_history = db.Column(db.Integer, primary_key=True, autoincrement=True)
    no_pasien = db.Column(db.Integer, db.ForeignKey('pasien.no_pasien'))
    username = db.Column(db.String(99), nullable=False)
    nama_pasien = db.Column(db.String(80), nullable=False)
    alamat_pasien = db.Column(db.String(80), nullable=False)
    flag = db.Column(db.String(2), nullable=False)
    created_date = db.Column(db.DateTime, nullable=False)
    updated_date = db.Column(db.DateTime, nullable=False)

    def __init__(self, no_pasien, username, nama_pasien, alamat_pasien, flag, created_date, updated_date):
        self.no_pasien = no_pasien
        self.username = username
        self.nama_pasien = nama_pasien
        self.alamat_pasien = alamat_pasien
        self.flag = flag
        self.created_date = created_date
        self.updated_date = updated_date
    
    def __repr__(self):
        return '<pasien_history %r>' % self.no_pasien_history