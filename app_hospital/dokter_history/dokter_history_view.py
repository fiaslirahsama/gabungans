from app_hospital.dokter_history import dokter_history_bp, dokter_history_controller

# This file work for routing function from the html to the controller file.

# The function below work for routing function to viewDokterHistory in the dokter_histor_controller using the blueprint connection.
@dokter_history_bp.route('/viewDokterHistory')
def viewDokterHistory():
    return dokter_history_controller.viewDokterHistory()

# The function below work for routing function to addDokterHistory in the dokter_histor_controller using the blueprint connection.
@dokter_history_bp.route('/addDokterHistory')
def addDokterHistory():
    return dokter_history_controller.addDokterHistory()