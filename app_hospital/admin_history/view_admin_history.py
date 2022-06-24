from app_hospital.admin_history import admin_history_bp, controller_admin_history, model_admin_history

@admin_history_bp.route('/addAdminHistory')
def addAdminHistory():
    controller_admin_history.addAdminHistory()
    return render_template("admin_history/admin_history.html")