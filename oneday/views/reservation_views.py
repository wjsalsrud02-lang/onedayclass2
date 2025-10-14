from flask import Blueprint, render_template, request, redirect, url_for, session, flash
from flask_login import login_required, current_user

from oneday.models import db, Reservation
import datetime

bp = Blueprint("reservations", __name__, url_prefix="/reservations")


@bp.before_app_request
def set_user():
    # 데모용: 로그인 없이 고정 user_id 사용
    session["user_id"] = 1


# 예약 목록
@bp.route("/")
def reservation_list():
    user_id = session.get("user_id")
    reservations = Reservation.query.filter_by(user_id=user_id).order_by(Reservation.reserved_date.desc()).all()
    return render_template("reservation/reservation_list.html", reservations=reservations)


# 예약 상세
@bp.route("/<int:res_id>")
def reservation_detail(res_id):
    reservation = Reservation.query.get_or_404(res_id)
    return render_template("reservation/reservation_detail.html", reservation=reservation)


# 예약 생성/수정
@bp.route("/new", methods=["GET", "POST"])
@bp.route("/<int:res_id>/edit", methods=["GET", "POST"])
def reservation_form(res_id=None):
    reservation = Reservation.query.get(res_id) if res_id else None

    if request.method == "POST":
        class_name = request.form["class_name"]
        reserved_date = request.form["reserved_date"]
        reserved_time = request.form["reserved_time"]

        if reservation:  # 수정
            reservation.class_name = class_name
            reservation.reserved_date = datetime.datetime.strptime(reserved_date, "%Y-%m-%d").date()
            reservation.reserved_time = reserved_time
            # 상태(status)는 수정 시 그대로 둠
        else:  # 새 예약
            new_res = Reservation(
                user_id=session["user_id"],
                class_name=class_name,
                reserved_date=datetime.datetime.strptime(reserved_date, "%Y-%m-%d").date(),
                reserved_time=reserved_time,
                status="대기중"   # 새 예약은 기본값으로 "대기중"
            )
            db.session.add(new_res)

        db.session.commit()
        return redirect(url_for("reservations.reservation_list"))

    return render_template("reservation/reservation_form.html", reservation=reservation)

@bp.route("/<int:res_id>/delete", methods=["POST"])
@login_required
def delete_reservation(res_id):
    reservation = Reservation.query.get_or_404(res_id)
    if reservation.user_id != current_user.id:
        flash("해당 예약을 삭제할 수 없습니다.")
        return redirect(url_for("reservations.reservation_list"))
    db.session.delete(reservation)
    db.session.commit()
    flash("예약이 삭제되었습니다.")
    return redirect(url_for("reservations.reservation_list"))


