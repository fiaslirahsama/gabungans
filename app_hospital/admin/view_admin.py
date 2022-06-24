from app_hospital.admin import admin_bp, controller_admin, model_admin
from app_hospital import login_required
from flask import render_template, redirect, url_for, request
from app_hospital import current_user

@admin_bp.route('/master_admin', methods=['POST', 'GET'])
@login_required
def master_admin():
    if request.method == 'POST':
        rows = controller_admin.searchAdmin()
    else:
        rows = controller_admin.viewAdmin()
    return render_template("admin/admin.html", datas=rows, username=current_user)

@admin_bp.route('/addAdmin', methods=['POST'])
@login_required
def addAdmin():
    controller_admin.addAdmin()
    return redirect(url_for('admin_bp.master_admin'))

@admin_bp.route('/deleteAdmin/<string:idAdmin>')
@login_required
def deleteAdmin(idAdmin):
    controller_admin.deleteAdmin(idAdmin)
    return redirect(url_for('admin_bp.master_admin'))

@admin_bp.route('/editAdmin/<string:idAdmin>', methods=['POST'])
@login_required
def editAdmin(idAdmin):
    controller_admin.editAdmin(idAdmin)
    return redirect(url_for('admin_bp.master_admin'))