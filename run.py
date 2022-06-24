from werkzeug.serving import run_simple # werkzeug development server
from app import *

if __name__ == '__main__':
    run_simple('localhost', 5000, application=app.wsgi_app, use_reloader=True, use_debugger=True, use_evalex=True)
    