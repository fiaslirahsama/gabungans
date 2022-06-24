from flask import render_template
from app_hospital.dashboard import dashboard_bp

# This function for Home / first view of the website

@dashboard_bp.route('/')
def dashboard():
    return render_template("dashboard/dashboard.html")