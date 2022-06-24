from app_hospital.pasien import pasien_bp, controller_pasien, model_pasien
from flask import render_template, redirect, request, url_for
from app_hospital import current_user, login_required

@pasien_bp.route('/master_pasien', methods=['POST','GET'])
@login_required
def master_pasien():
    if request.method == 'POST':
        rows = controller_pasien.searchPasien()
    else:
        rows = controller_pasien.viewPasien()
    return render_template('pasien/pasien.html', username=current_user, datas=rows)

@pasien_bp.route('/add_pasien', methods=['POST'])
@login_required
def add_pasien():
    controller_pasien.addPasien()
    return redirect(url_for('pasien_bp.master_pasien'))

@pasien_bp.route('/edit_pasien/<string:no_pasien>', methods=['POST'])
@login_required
def edit_pasien(no_pasien):
    controller_pasien.editPasien(no_pasien)
    return redirect(url_for('pasien_bp.master_pasien'))

@pasien_bp.route('/delete_pasien/<string:no_pasien>')
@login_required
def delete_pasien(no_pasien):
    controller_pasien.deletePasien(no_pasien)
    return redirect(url_for('pasien_bp.master_pasien'))
        