# Berisi routing untuk menjalankan fungsi controller menggunakan url
from app_perpus.member import bp_member, member_controller
from app_perpus.auth.auth_controller import login_required
from flask import redirect, render_template, url_for

#MENAMPILKAN DATA MEMBER
@bp_member.route('/datamember', methods=['GET', 'POST'])
def data_member():
    generateid = member_controller.dataMember()
    members, ci, cni, cna, cj, ca = member_controller.searchMember()
    return render_template('member/datamember.html', generateid=generateid, members=members, ci=ci, cni=cni, cna=cna, cj=cj, ca=ca)

# MENAMBAHKAN DATA MEMBER
@bp_member.route('/tambahmember', methods=['GET', 'POST'])
@login_required
def tambah_member():
    member_controller.tambahMember()
    return redirect(url_for('member.data_member'))

# FITUR PENCARIAN DATA MEMBER
@bp_member.route('/searchmember', methods=['GET', 'POST'])
def search_member():
    return member_controller.searchMember()

# MENDOWNLOAD/EXPORT DATA MEMBER DALAM BENTUK CSV
@bp_member.route('/downloadmember', methods=['GET', 'POST'])
@login_required
def download_member():
    return member_controller.downloadMember()

# DOWNLOAD FORMAT UPLOAD CSV DATA MEMBER
@bp_member.route('/downloadformatmember', methods=['GET', 'POST'])
@login_required
def download_format_member():
    return member_controller.downloadFormatMember()

# MENAMBAH DATA BUKU DENGAN UPLOAD CSV
@bp_member.route('/uploadmember', methods=['GET', 'POST'])
@login_required
def upload_member():
    member_controller.uploadMember()
    return redirect(url_for('member.data_member'))

# MENGUPDATE / MENGEDIT DATA MEMBER
@bp_member.route('/updatemember/<int:id>', methods=['GET', 'POST'])
@login_required
def update_member(id):
    renderself, getmember = member_controller.updateMember(id)
    if renderself == False:
        return redirect(url_for('member.data_member'))
    return render_template('member/updatemember.html', getmember=getmember)

# MENGHAPUS DATA MEMBER
@bp_member.route('/deletemember/<int:id>', methods=['POST'])
@login_required
def delete_member(id):
    member_controller.deleteMember(id)
    return redirect(url_for('member.data_member'))