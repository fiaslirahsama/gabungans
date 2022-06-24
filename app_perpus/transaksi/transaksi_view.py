# Berisi routing untuk menjalankan fungsi controller menggunakan url
from app_perpus.transaksi import bp_transaksi, transaksi_controller
from app_perpus.auth.auth_controller import login_required
from flask import redirect, render_template, url_for

@bp_transaksi.route('/', methods=['GET', 'POST'])
def index():
    transaksis, cp, cj, cw1, cw2 = transaksi_controller.index()
    return render_template('transaksi/index.html', transaksis=transaksis, cp=cp, cj=cj, cw1=cw1, cw2=cw2)

@bp_transaksi.route('/downloadtransaksi', methods=('GET','POST'))
@login_required
def downloadtransaksi():
    transaksi_controller.downloadtransaksi()
    return redirect(url_for('index')) 

@bp_transaksi.route('/tambahtransaksi', methods=('GET', 'POST'))
@login_required
def tambahtransaksi():
    transaksi_controller.tambahtransaksi()
    return redirect(url_for('index')) 

@bp_transaksi.route('/updatetransaksi/<int:id>', methods=('GET', 'POST'))
@login_required
def updatetransaksi(id):
    renderself, gettransaksi = transaksi_controller.updatetransaksi(id)
    if renderself == False:
        return redirect(url_for('index'))
    return render_template('transaksi/updatetransaksi.html', gettransaksi=gettransaksi)