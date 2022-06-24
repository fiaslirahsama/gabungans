from app_hospital.pasien import pasien_bp, pasien_controller

# This file work for routing function from the html to the controller file.

# The function below work for routing function to viewPasien in the pasien_controller using the blueprint connection.
@pasien_bp.route('/viewPasien')
def viewPasien():
    return pasien_controller.viewPasien()

# The function below work for routing function to addPasien in the pasien_controller using the blueprint connection.
@pasien_bp.route('/addPasien', methods=['POST'])
def addPasien():
    return pasien_controller.addPasien()

# The function below work for routing function to editPasien in the pasien_controller using the blueprint connection.
@pasien_bp.route('/editPasien/<string:idPasien>', methods=['POST'])
def editPasien(idPasien):
    return pasien_controller.editPasien(idPasien)

# The function below work for routing function to deletePasien in the pasien_controller using the blueprint connection.
@pasien_bp.route('/deletePasien/<string:idPasien>', methods=['GET'])
def deletePasien(idPasien):
    return pasien_controller.deletePasien(idPasien)

# The function below work for routing function to searchPasien in the pasien_controller using the blueprint connection.
@pasien_bp.route('/searchPasien', methods=['POST'])
def searchPasien():
    return pasien_controller.searchPasien()

# The function below work for routing function to importFilePasien in the pasien_controller using the blueprint connection.
@pasien_bp.route('/importFilePasien', methods=['POST'])
def importFilePasien():
    return pasien_controller.importFilePasien()

# The function below work for routing function to downloadTemplatePasien in the pasien_controller using the blueprint connection.
@pasien_bp.route('/downloadTemplatePasien')
def downloadTemplatePasien():
    return pasien_controller.downloadTemplatePasien()