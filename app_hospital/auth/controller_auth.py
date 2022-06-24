from flask import *
from app_hospital.auth.model_auth import auth
from app_hospital import login_user, logout_user, db
import datetime

def addAuth(username, password, status_auth):
    try:
        date = datetime.datetime.now()
        newUser = auth(username=username, status_auth=status_auth, password=generate_password_hash(password, method='sha256'), flag="Y", created_date=date, updated_date=date)
        db.session.add(newUser)
        db.session.commit()
        db.session.close()
    except Exception as e:
        return flash(e)

def findIdAuth(username):
    try:
        username = username
        find = auth.query.filter(auth.username==username, auth.flag=="Y").first()
        db.session.close()
        return find.id_auth
    except Exception as e:
        return flash(e)
