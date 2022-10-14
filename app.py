from werkzeug.middleware.dispatcher import DispatcherMiddleware # use to combine each Flask app into a larger one that is dispatched based on prefix
# from flask_sqlalchemy import SQLAlchemy
# from flask_migrate import Migrate
from app_perpus import create_app_perpus 
from app_hospital import create_app_hospital 

app_perpus = create_app_perpus()
app = create_app_hospital()

multiapp = DispatcherMiddleware(app, {
    '/perpus': app_perpus
})