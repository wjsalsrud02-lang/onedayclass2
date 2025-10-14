from flask_wtf import FlaskForm

from wtforms.fields.numeric import IntegerField
from wtforms.fields.simple import StringField, TextAreaField, PasswordField, EmailField, BooleanField, SubmitField
from wtforms.validators import DataRequired, Length, EqualTo, Email, NumberRange
from flask_wtf.file import FileField, FileAllowed, FileRequired, MultipleFileField
from wtforms.validators import Optional



class QuestionForm(FlaskForm):
    subject = StringField('제목', validators=[DataRequired('제목은 필수입력 항목입니다.')])
    content = TextAreaField('내용', validators=[DataRequired('내용은 필수입력 항목입니다.')])
    image = FileField('이미지 업로드', validators=[FileAllowed(['jpg', 'jpeg', 'png', 'gif'], '이미지 파일만 업로드 가능합니다.')])
    submit = SubmitField('저장하기')

class AnswerForm(FlaskForm):
    content = TextAreaField('내용', validators=[DataRequired('내용은 필수입력 항목입니다.')])

class UserCreateForm(FlaskForm):
    username = StringField('사용자이름', validators=[DataRequired(), Length(min=3, max=25)])
    password1 = PasswordField('비밀번호', validators=[DataRequired(), EqualTo('password2', message='비밀번호가 일치하지 않습니다.')])
    password2 = PasswordField('비밀번호확인', validators=[DataRequired()])
    email = EmailField('이메일', validators=[DataRequired(), Email()])

class UserLoginForm(FlaskForm):
    username = StringField('사용자이름', validators=[DataRequired(), Length(min=3, max=25)])
    password = PasswordField('비밀번호', validators=[DataRequired()])

class CourseCreateForm(FlaskForm):
    classid = StringField("클래스 ID", validators=[DataRequired(), Length(min=3, max=50)])
    description = TextAreaField("설명", validators=[DataRequired(), Length(min=5)])
    price = IntegerField("가격", validators=[DataRequired(),NumberRange(min=0) ],default=0)
    duration_minutes = IntegerField("소요시간", validators=[NumberRange(min=5)], default=60)
    is_published = BooleanField("등록 완료 여부")
    image = FileField('이미지 업로드', validators=[FileRequired(message="대표 이미지를 반드시 업로드해야 합니다."),FileAllowed(['jpg', 'jpeg', 'png', 'gif'], '이미지 파일만 업로드 가능합니다.')])
    images = MultipleFileField(
        "추가 이미지 (최대 4장)",
        validators=[FileAllowed(['jpg', 'jpeg', 'png', 'gif'], "이미지 파일만 업로드 가능합니다.")]
    )

