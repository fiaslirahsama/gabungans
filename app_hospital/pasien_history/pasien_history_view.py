from app_hospital.pasien_history import pasien_history_bp, pasien_history_controller

# This file work for routing function from the html to the controller file.

# The function below work for routing function to addPasienHistory in the pasien_history_controller using the blueprint connection.
@pasien_history_bp.route('/addPasienHistory')
def addPasienHistory():
    return pasien_history_controller.addPasienHistory()

# The function below work for routing function to viewPasienHistory in the pasien_history_controller using the blueprint connection.
@pasien_history_bp.route('/viewPasienHistory')
def viewPasienHistory():
    return pasien_history_controller.viewPasienHistory()