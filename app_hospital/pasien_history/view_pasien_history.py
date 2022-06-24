from app_hospital.pasien_history import pasien_history_bp, controller_pasien_history, model_pasien_history

@pasien_history_bp.route('/viewPasienHistory')
def viewPasienHistory():
    pasien_history_controller.viewPasienHistory()
    return render_template("pasien_history.view_pasien_history.html")