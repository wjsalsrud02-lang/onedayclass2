from datetime import datetime
from flask import Blueprint, request, redirect, url_for, render_template, flash
from flask_login import current_user, login_required
from oneday import db
from oneday.forms import AnswerForm
from oneday.models import Question, Answer

bp = Blueprint('answer', __name__, url_prefix='/answer')

@bp.route('/create/<int:question_id>', methods=['POST'])
@login_required
def create(question_id):
    form = AnswerForm()
    question = Question.query.get_or_404(question_id)
    if form.validate_on_submit():
        content = form.content.data
        answer = Answer(content=content, create_date=datetime.now(), user=current_user)
        question.answer_set.append(answer)
        db.session.commit()
        return redirect(url_for('question.detail', question_id=question_id))
    return render_template('question/question_detail.html', question=question, form=form)

@bp.route('/modify/<int:answer_id>/', methods=['GET','POST'])
@login_required
def modify(answer_id):
    answer = Answer.query.get_or_404(answer_id)
    if current_user != answer.user:
        flash('수정 권한이 없습니다.')
        return redirect(url_for('question.detail', question_id=answer.question.id))
    form = AnswerForm(obj=answer)
    if request.method == 'POST' and form.validate_on_submit():
        form.populate_obj(answer)
        answer.modify_date = datetime.now()
        db.session.commit()
        return redirect(url_for('question.detail', question_id=answer.question.id))
    return render_template('answer/answer_form.html', form=form)

@bp.route('/delete/<int:answer_id>/')
@login_required
def delete(answer_id):
    answer = Answer.query.get_or_404(answer_id)

    if current_user != answer.user:
        flash('삭제 권한이 없습니다.')
        return redirect(url_for('question.detail', question_id=answer.question_id))

    # 삭제 전에 question_id 저장
    question_id = answer.question_id
    db.session.delete(answer)
    db.session.commit()
    return redirect(url_for('question.detail', question_id=question_id))




