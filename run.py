from werkzeug.serving import run_simple # werkzeug development server
# from app_perpus import create_app_perpus
# from app_hospital import create_app_hospital
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from app import multiapp, app, app_perpus


dblo = SQLAlchemy()
migrain = Migrate()
migroin = Migrate()
# app2 = create_app_perpus()
# print(app2)
# app = create_app_hospital()
# print(app)
migrain.init_app(app, dblo)
migrain.app = app
migroin.init_app(app_perpus, dblo)
migroin.app = app_perpus

if __name__ == '__main__':
    # app2.run('localhost', 5001, threaded=True)
    # app.run('localhost', 5000, threaded=True)
    run_simple('localhost', 5000, application=multiapp, use_reloader=True, use_debugger=True, use_evalex=True, threaded=True)
    # run_simple('localhost', 5001, application=app2, use_reloader=True, use_debugger=True, use_evalex=True, threaded=True)
    