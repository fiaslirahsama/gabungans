from flask_sqlalchemy import SQLAlchemy
from app_hospital import db
from app_hospital.dokter.model_dokter import dokter
from app_hospital.pasien.model_pasien import pasien

# This file work for define and initialize model for the database.

class trans(db.Model):
    id_trans = db.Column(db.Integer, primary_key=True, autoincrement=True)
    id_dokter = db.Column(db.Integer, db.ForeignKey('dokter.id_dokter'))
    no_pasien = db.Column(db.Integer, db.ForeignKey('pasien.no_pasien'))
    status_bayar = db.Column(db.String(2), nullable=False)
    status_checking_dokter = db.Column(db.String(2), nullable=False)
    resep_dokter = db.Column(db.String(99), nullable=False)
    harga_bayar = db.Column(db.Integer, nullable=False)
    keluhan = db.Column(db.String(99), nullable=False)
    flag = db.Column(db.String(2), nullable=False)
    created_date = db.Column(db.DateTime, nullable=False)
    updated_date = db.Column(db.DateTime, nullable=False)

    def __init__(self, id_dokter, no_pasien, status_bayar, status_checking_dokter, resep_dokter, keluhan, harga_bayar, flag, created_date, updated_date):
        self.id_dokter = id_dokter
        self.no_pasien = no_pasien
        self.status_bayar = status_bayar
        self.status_checking_dokter = status_checking_dokter
        self.resep_dokter = resep_dokter
        self.harga_bayar = harga_bayar
        self.keluhan = keluhan
        self.flag = flag
        self.created_date = created_date
        self.updated_date = updated_date
    
    def __repr__(self):
        return '<trans %r>' % self.id_trans