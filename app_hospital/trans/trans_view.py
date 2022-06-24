from app_hospital.trans import trans_controller, trans_bp

# This file work for routing function from the html to the controller file.

# The function below work for routing function to viewTrans in the trans_controller using the blueprint connection.
@trans_bp.route('/viewTrans')
def viewTrans():
    return trans_controller.viewTrans()

# The function below work for routing function to searchTrans in the trans_controller using the blueprint connection.
@trans_bp.route('/searchTrans', methods=['POST'])
def searchTrans():
    return trans_controller.searchTrans()

# The function below work for routing function to showAvailableDokter in the trans_controller using the blueprint connection.
@trans_bp.route('/showAvailableDokter')
def showAvailableDokter():
    return trans_controller.showAvailableDokter()

# The function below work for routing function to bookDokter in the trans_controller using the blueprint connection.
@trans_bp.route('/bookDokter', methods=['POST'])
def bookDokter():
    return trans_controller.bookDokter()

# The function below work for routing function to saveDokterResult in the trans_controller using the blueprint connection.
@trans_bp.route('/saveDokterResult', methods=['POST'])
def saveDokterResult():
    return trans_controller.saveDokterResult()

# The function below work for routing function to payment in the trans_controller using the blueprint connection.
@trans_bp.route('/payment', methods=['POST'])
def payment():
    return trans_controller.payment()

# The function below work for routing function to showDokterInTrans in the trans_controller using the blueprint connection.
@trans_bp.route('/showDokterInTrans')
def showDokterInTrans():
    return trans_controller.showDokterInTrans()

# The function below work for routing function to searchDokterInTrans in the trans_controller using the blueprint connection.
@trans_bp.route('/searchDokterInTrans', methods=['POST'])
def searchDokterInTrans():
    return trans_controller.searchDokterInTrans()

# The function below work for routing function to searchAvailableDokter in the trans_controller using the blueprint connection.
@trans_bp.route('/searchAvailableDokter', methods=['POST'])
def searchAvailableDokter():
    return trans_controller.searchAvailableDokter()

# The function below work for routing function to showPaymentList in the trans_controller using the blueprint connection.
@trans_bp.route('/showPaymentList')
def showPaymentList():
    return trans_controller.showPaymentList()

# The function below work for routing function to savePayment in the trans_controller using the blueprint connection.
@trans_bp.route('/savePayment', methods=['POST'])
def savePayment():
    return trans_controller.savePayment()

# The function below work for routing function to searchPaymentList in the trans_controller using the blueprint connection.
@trans_bp.route('/searchPaymentList', methods=['POST'])
def searchPaymentList():
    return trans_controller.searchPaymentList()