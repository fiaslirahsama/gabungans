# Berisi routing untuk menjalankan fungsi controller menggunakan url
from app_perpus.buku import bp_buku, buku_controller
from app_perpus.auth.auth_controller import login_required
from flask import redirect, render_template, url_for

# MENAMPILKAN DATA BUKU
@bp_buku.route('/databuku', methods=['GET', 'POST'])
def data_buku():
    generate_id = buku_controller.dataBuku()
    bukus, ci, cj, cg, cp, ca = buku_controller.searchBuku()
    return render_template('buku/databuku.html', generate_id=generate_id, bukus=bukus, ci=ci, cj=cj, cg=cg, cp=cp, ca=ca)

# FUNGSI MENAMPILKAN DATA KODE RAK BUKU DAN KODE GENRE
@bp_buku.route('/datakode', methods=['GET', 'POST'])
def data_kode():
    koderaks = buku_controller.dataKode()[0]
    kodegenres = buku_controller.dataKode()[1]
    return render_template('buku/datakode.html', koderak=koderaks, kodegenre=kodegenres)

# MENAMBAH DATA BUKU
@bp_buku.route('/tambahbuku', methods=['GET', 'POST'])
def tambah_buku():
    buku_controller.tambahBuku()
    return redirect(url_for('buku.data_buku'))

# MENAMBAH DATA KODE RAK
@bp_buku.route('/tambahkoderak', methods=['GET', 'POST'])
def tambah_kode_rak():
    buku_controller.tambahKodeRak()
    return redirect(url_for('buku.data_kode'))

# MENAMBAH DATA KODE GENRE
@bp_buku.route('/tambahkodegenre', methods=['GET', 'POST'])
def tambah_kode_genre():
    buku_controller.tambahKodeGenre()
    return redirect(url_for('buku.data_kode'))

# MENAMBAH DATA BUKU DENGAN UPLOAD CSV
@bp_buku.route('/uploadbuku', methods=['GET', 'POST'])
@login_required
def upload_buku():
    buku_controller.uploadBuku()
    return redirect(url_for('buku.data_buku'))

# FITUR PENCARIAN DATA BUKU
@bp_buku.route('/searchbuku', methods=['GET', 'POST'])
def search_buku():
    return buku_controller.searchBuku()

# MENGUPDATE / MENGEDIT DATA BUKU YANG MASIH TERSEDIA
@bp_buku.route('/updatebukuada/<int:id>', methods=['GET', 'POST'])
@login_required
def update_buku_ada(id):
    renderself, getbuku = buku_controller.updateBukuAda(id)
    if renderself == False:
        return redirect(url_for('buku.data_buku'))
    return render_template('buku/updatebukuada.html', getbuku=getbuku)

# MENGUPDATE / MENGEDIR DATA BUKU YANG TELAH DIPINJAM
@bp_buku.route('/updatebukudipinjam/<int:id>', methods=['GET', 'POST'])
@login_required
def update_buku_dipinjam(id):
    renderself, getbuku = buku_controller.updateBukuDipinjam(id)
    if renderself == False:
        return redirect(url_for('buku.data_buku'))
    return render_template('buku/updatebukudipinjam.html', getbuku=getbuku)

# MENGUPDATE / MENGEDIT DATA KODE RAK
@bp_buku.route('/updatekoderak/<int:id>', methods=['GET', 'POST'])
@login_required
def update_kode_rak(id):
    print(id)
    # renderself, getbuku = buku_controller.updateBukuAda(id)
    # if renderself == False:
    #     return redirect(url_for('buku.data_buku'))
    # return render_template('buku/updatebukuada.html', getbuku=getbuku)

# MENGUPDATE / MENGEDIT DATA KODE GENRE
@bp_buku.route('/updatekodegenre/<int:id>', methods=['GET', 'POST'])
@login_required
def update_kode_genre(id):
    print(id)
    # renderself, getbuku = buku_controller.updateBukuAda(id)
    # if renderself == False:
    #     return redirect(url_for('buku.data_buku'))
    # return render_template('buku/updatebukuada.html', getbuku=getbuku)

# MENGHAPUS DATA BUKU
@bp_buku.route('/deletebuku/<int:id>', methods=['POST'])
@login_required
def delete_buku(id):
    buku_controller.deleteBuku(id)
    return redirect(url_for('buku.data_buku'))

# MENGHAPUS DATA KODE RAK
@bp_buku.route('/deletekoderak/<int:id>', methods=['POST'])
@login_required
def delete_kode_rak(id):
    print(id)
    # buku_controller.deleteBuku(id)
    # return redirect(url_for('buku.data_buku'))

# MENGHAPUS DATA KODE GENRE
@bp_buku.route('/deletekodegenre/<int:id>', methods=['POST'])
@login_required
def delete_kode_genre(id):
    print(id)
    # buku_controller.deleteBuku(id)
    # return redirect(url_for('buku.data_buku'))

# MENDOWNLOAD/EXPORT DATA BUKU DALAM BENTUK CSV
@bp_buku.route('/downloadbuku', methods=['GET', 'POST'])
@login_required
def download_buku():
    return buku_controller.downloadBuku()

# DOWNLOAD FORMAT UPLOAD CSV DATA BUKU
@bp_buku.route('/downloadformatbuku', methods=['GET', 'POST'])
@login_required
def download_format_buku():
    return buku_controller.downloadFormatBuku()