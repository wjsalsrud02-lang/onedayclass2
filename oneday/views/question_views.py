import os
from datetime import datetime
from flask import Blueprint, render_template, request, url_for, redirect, flash, current_app
from flask_login import login_required, current_user
from werkzeug.utils import secure_filename
from oneday import db
from oneday.forms import QuestionForm, AnswerForm
from oneday.models import Question

bp = Blueprint('question', __name__, url_prefix='/question')

@bp.route('/list/')
def _list():
    page = request.args.get('page', 1, type=int)
    questions = Question.query.order_by(Question.create_date.desc()).paginate(page=page, per_page=30)
    return render_template('question/question_list.html', question_list=questions)

@bp.route('/detail/<int:question_id>/')
def detail(question_id):
    question = Question.query.get_or_404(question_id)
    form = AnswerForm()
    return render_template('question/question_detail.html', question=question, form=form)

@bp.route('/create/', methods=['GET','POST'])
@login_required
def create():
    form = QuestionForm()
    if request.method == 'POST' and form.validate_on_submit():
        image_file = form.image.data
        image_path = None
        if image_file:
            today = datetime.now().strftime('%Y%m%d')
            upload_folder = os.path.join(current_app.root_path, 'static/photo', today)
            os.makedirs(upload_folder, exist_ok=True)
            filename = secure_filename(image_file.filename)
            image_file.save(os.path.join(upload_folder, filename))
            image_path = f'photo/{today}/{filename}'

        question = Question(
            subject=form.subject.data,
            content=form.content.data,
            create_date=datetime.now(),
            user_id=current_user.id,
            image_path=image_path
        )
        db.session.add(question)
        db.session.commit()
        return redirect(url_for('question._list'))
    return render_template('question/question_form.html', form=form)

@bp.route('/modify/<int:question_id>/', methods=['GET','POST'])
@login_required
def modify(question_id):
    question = Question.query.get_or_404(question_id)
    if current_user != question.user:
        flash('수정 권한이 없습니다.')
        return redirect(url_for('question.detail', question_id=question_id))
    form = QuestionForm(obj=question)
    if request.method == 'POST' and form.validate_on_submit():
        form.populate_obj(question)
        question.modify_date = datetime.now()
        db.session.commit()
        return redirect(url_for('question.detail', question_id=question_id))
    return render_template('question/question_form.html', form=form)

@bp.route('/delete/<int:question_id>/')
@login_required
def delete(question_id):
    question = Question.query.get_or_404(question_id)
    if current_user != question.user:
        flash('삭제 권한이 없습니다.')
        return redirect(url_for('question.detail', question_id=question_id))
    db.session.delete(question)
    db.session.commit()
    return redirect(url_for('question._list'))
