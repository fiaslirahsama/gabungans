from app_hospital.trans import trans_bp, controller_trans, model_trans
from app_hospital.pasien.model_pasien import pasien
from app_hospital.dokter.model_dokter import dokter
from app_hospital.dokter import controller_dokter
from app_hospital.pasien import controller_pasien
from flask import render_template, redirect, request, url_for
from app_hospital import current_user, login_required

# FOR SUPER ADMIN TO SHOW RECORD TRANS
@trans_bp.route('/master_trans', methods=['POST', 'GET'])
@login_required
def master_trans():
    if request.method == 'POST':
        rows = controller_trans.searchTrans()
    else:
        rows = controller_trans.viewTrans()
    return render_template('trans/trans.html', username=current_user, datas=rows)

# FOR PASIEN MENU BOOK DOKTER
@trans_bp.route('/show_dokter', methods=['POST', 'GET'])
@login_required
def show_dokter():
    if request.method == 'POST' and request.form.get('search-available-dokter'):
        rows = controller_trans.searchAvailableDokter(id_dokter, nama_dokter, hari_kerja, jam_kerja)
        rows2 = controller_pasien.viewPasien()
        return render_template('trans/available_dokter.html', datas = rows, datas2=rows2, username=current_user)
    if request.method == 'POST' and not request.form.get('search-available-dokter'):
        controller_trans.bookDokter()
        return redirect(url_for('trans_bp.show_dokter'))
    else:
        rows = controller_trans.showDokter()
        rows2 = controller_pasien.findPasienWithUsername(current_user.username)
        return render_template('trans/available_dokter.html', datas = rows, datas2=rows2, username=current_user)

# FOR DOKTER MENU CHECKING PASIEN
@trans_bp.route('/checking_dokter', methods=['POST', 'GET'])
@login_required
def checking_dokter():
    if request.method == 'POST':
        controller_trans.saveDokterResult()
        return redirect(url_for('trans_bp.checking_dokter'))
    else:
        rows = controller_trans.checkingDokter()
    return render_template("trans/checking_dokter.html", datas=rows, username=current_user)

# FOR ADMIN TO CHECK DOKTER THAT HAVE TRANS / BOOKING
@trans_bp.route('/dokter_trans', methods=['POST', 'GET'])
@login_required
def dokter_trans():
    if request.method == 'POST':
        rows = controller_trans.searchDokterInTrans()
    else:
        rows = controller_trans.showDokterTrans()
    return render_template('trans/dokter_trans.html', datas = rows, username=current_user)

# FOR ADMIN TO SAVE PAYMENT AND SHOW PAYMENT LIST
@trans_bp.route('/payment', methods=['POST', 'GET'])
@login_required
def payment():
    if request.method == 'POST' and not request.form.get('add_payment'):
        print("tis")
        rows = controller_trans.searchPayment()
        return render_template('trans/payment.html', datas=rows, username=current_user)
    elif request.method == 'POST' and request.form.get('add_payment'):
        print("tes")
        controller_trans.savePayment()
        return redirect(url_for('trans_bp.payment'))
    else:
        rows = controller_trans.paymentList()
        return render_template('trans/payment.html', datas=rows, username=current_user)

# FOR PASIEN CHECK DETAIL BOOK
@trans_bp.route('/detail_book_pasien')
def detail_book_pasien():
    rows = controller_trans.detailBookPasien()
    return render_template('trans/detail_book.html', datas=rows, username=current_user)