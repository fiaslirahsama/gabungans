from app_hospital.dokter import dokter_bp, controller_dokter, model_dokter
from flask import render_template, redirect, request, url_for
from app_hospital import current_user, login_required

@dokter_bp.route('/master_dokter', methods=['POST', 'GET'])
@login_required
def master_dokter():
    if request.method == 'POST':
        dokter = controller_dokter.searchDokter()
    else:
        dokter = controller_dokter.viewDokter()
    return render_template('dokter/dokter.html', username=current_user, datas=dokter)

@dokter_bp.route('/add_dokter', methods=['POST'])
@login_required
def add_dokter():
    controller_dokter.addDokter()
    return redirect(url_for('dokter_bp.master_dokter'))

@dokter_bp.route('/edit_dokter/<string:id_dokter>', methods=['POST'])
@login_required
def edit_dokter(id_dokter):
    controller_dokter.editDokter(id_dokter)
    return redirect(url_for('dokter_bp.master_dokter'))

@dokter_bp.route('/delete_dokter/<string:id_dokter>')
@login_required
def delete_dokter(id_dokter):
    controller_dokter.deleteDokter(id_dokter)
    return redirect(url_for('dokter_bp.master_dokter'))

@dokter_bp.route('/download_template_dokter')
@login_required
def download_template_dokter():
    return controller_dokter.downloadTemplateDokter()

@dokter_bp.route('/import_add_dokter', methods=['POST'])
@login_required
def import_add_dokter():
    controller_dokter.importAddDokter()
    return redirect(url_for('dokter_bp.master_dokter'))
