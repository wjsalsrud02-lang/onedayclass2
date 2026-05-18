from flask import Flask
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
import config
import os

db = SQLAlchemy()
migrate = Migrate()


login_manager = LoginManager()
login_manager.login_view = "auth.login"

def create_app():
    app = Flask(__name__)
    app.config.from_object(config)

    os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

    # 확장 초기화
    db.init_app(app)
    migrate.init_app(app, db)
    from . import models


    login_manager.init_app(app)


    from .models import User
    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))

    # 블루프린트 등록
    from .views import (
        main_views, question_views, answer_views,
        auth_views, course_views, reservation_views, sub_views
    )
    app.register_blueprint(main_views.bp)
    app.register_blueprint(question_views.bp)
    app.register_blueprint(answer_views.bp)
    app.register_blueprint(auth_views.bp)
    app.register_blueprint(course_views.bp)
    app.register_blueprint(reservation_views.bp)
    app.register_blueprint(sub_views.bp)

    # 필터
    from .filter import format_datetime
    app.jinja_env.filters['datetime'] = format_datetime

    return app
