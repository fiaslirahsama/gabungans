from app_hospital.dokter import dokter_controller, dokter_bp

# This file work for routing function from the html to the controller file.

# The function below work for routing function to viewDokter in the dokter_controller using the blueprint connection.
@dokter_bp.route('/viewDokter')
def viewDokter():
    return dokter_controller.viewDokter()

# The function below work for routing function to addDokter in the dokter_controller using the blueprint connection.
@dokter_bp.route('/addDokter', methods=['POST'])
def addDokter():
    return dokter_controller.addDokter()

# The function below work for routing function to editDokter in the dokter_controller using the blueprint connection.
@dokter_bp.route('/editDokter/<string:idDokter>', methods=['POST'])
def editDokter(idDokter):
    return dokter_controller.editDokter(idDokter)

# The function below work for routing function to deleteDokter in the dokter_controller using the blueprint connection.
@dokter_bp.route('/deleteDokter/<string:idDokter>', methods=['GET'])
def deleteDokter(idDokter):
    return dokter_controller.deleteDokter(idDokter)

# The function below work for routing function to searchDokter in the dokter_controller using the blueprint connection.
@dokter_bp.route('/searchDokter', methods=['POST'])
def searchDokter():
    return dokter_controller.searchDokter()

# The function below work for routing function to importFileDokter in the dokter_controller using the blueprint connection.
@dokter_bp.route('/importFileDokter', methods=['POST'])
def importFileDokter():
    return dokter_controller.importFileDokter()

# The function below work for routing function to downloadTemplateDokter in the dokter_controller using the blueprint connection.
@dokter_bp.route('/downloadTemplateDokter')
def downloadTemplateDokter():
    return dokter_controller.downloadTemplateDokter()