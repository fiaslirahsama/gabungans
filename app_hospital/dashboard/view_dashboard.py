from flask import render_template
from app_hospital.dashboard import dashboard_bp
from app_hospital import login_required, current_user

# This function for Home / first view of the website

@dashboard_bp.route('/home')
@login_required
def dashboard():
    return render_template("dashboard/dashboard.html", username=current_user)