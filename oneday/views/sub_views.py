from flask import Blueprint, render_template

# 블루프린트 생성
bp = Blueprint('sub', __name__, url_prefix='/')

@bp.route('/about')
def about():
    return render_template('about.html')

@bp.route('/about2')
def about2():
    return render_template('about2.html')

@bp.route('/about3')
def about3():
    return render_template('about3.html')

@bp.route('/about4')
def about4():
    return render_template('about4.html')

@bp.route('/about5')
def about5():
    return render_template('about5.html')

@bp.route('/about6')
def about6():
    return render_template('about6.html')

@bp.route('/about7')
def about7():
    return render_template('about7.html')

@bp.route('/about8')
def about8():
    return render_template('about8.html')