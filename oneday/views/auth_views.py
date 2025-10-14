from flask import Blueprint, request, redirect, url_for, flash, render_template, make_response, session
from flask_login import login_user, logout_user, login_required, current_user
from werkzeug.security import generate_password_hash

from oneday import db
from oneday.forms import UserCreateForm, UserLoginForm
from oneday.models import User

bp = Blueprint('auth', __name__, url_prefix='/auth')


# 마이페이지
@bp.route("/mypage")
@login_required
def mypage():
    return render_template("auth/mypage.html", user=current_user)


# 회원가입
@bp.route("/signup", methods=["GET", "POST"])
def signup():
    form = UserCreateForm()
    if form.validate_on_submit():
        name = form.username.data
        email = form.email.data
        password1 = form.password1.data
        password2 = form.password2.data

        if password1 != password2:
            flash("비밀번호가 일치하지 않습니다.", "danger")
        else:
            existing_user = User.query.filter_by(email=email).first()
            if existing_user:
                flash("이미 존재하는 이메일입니다.", "danger")
            else:
                user = User(
                    username=name,
                    email=email,
                    password=generate_password_hash(password1)
                )
                db.session.add(user)
                db.session.commit()
                flash("회원가입이 완료되었습니다.", "success")
                return redirect(url_for("auth.login"))

    return render_template("auth/signup.html", form=form)


# 로그인
@bp.route("/login", methods=["GET", "POST"])
def login():
    form = UserLoginForm()
    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data

        user = User.query.filter_by(username=username).first()
        if user and user.check_password(password):
            login_user(user)  # 로그인 처리
            flash(f"{user.username}님 환영합니다!", "success")
            next_page = request.args.get('next')
            return redirect(next_page or url_for("auth.mypage"))
        else:
            flash("사용자이름 또는 비밀번호가 올바르지 않습니다.", "danger")

    return render_template("auth/login.html", form=form)


@bp.route("/logout")
@login_required
def logout():
    session.clear()
    return redirect(url_for("auth.login"))
