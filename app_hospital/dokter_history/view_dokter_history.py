from app_hospital.dokter_history import dokter_history_bp, controller_dokter_history, model_dokter_history

@dokter_history_bp.route('/addDokterHistory')
def addDokterHistory():
    controller_dokter.addDokterHistory()
    return render_template("dokter_history/dokter_history.html")