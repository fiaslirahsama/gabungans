# MELAKUKAN INISIASI APLIKASI PADA SAAT FLASK DIJALANKAN
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
# from flask_migrate import Migrate
from config import DevelopmentConfig
import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from flask_mysqldb import MySQL

db = SQLAlchemy()
# migrate2 = Migrate()

def create_app_perpus(config=DevelopmentConfig):
    app = Flask(__name__)
    print('perp', app)
    app.config.from_object(config)

    db.init_app(app)
    db.app = app

    #Jalankan Flask db init dan db migrate dan db upgrade dulu untuk kali pertama
    # migrate2.init_app(app, db)
    # migrate2.app = app

    # mendaftarkan blueprint folder auth, buku, member, transaksi pada main app

    from app_perpus.auth import bp_auth as auth
    app.register_blueprint(auth)

    from app_perpus.buku import bp_buku as buku
    app.register_blueprint(buku)

    from app_perpus.member import bp_member as member
    app.register_blueprint(member)

    from app_perpus.transaksi import bp_transaksi as transaksi
    app.register_blueprint(transaksi)

    app.add_url_rule('/', endpoint='index')
    db.create_all()

    return app