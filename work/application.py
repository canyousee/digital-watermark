# -*- coding: UTF-8 -*-
from flask import Flask, redirect, url_for
from templates import AdminLTE
from blueprints import all_blueprints
from importlib import import_module
from extentions import login_manager
from extentions import db
from config import config
import os
from werkzeug.security import generate_password_hash
from flask_script import Manager
from flask_migrate import Migrate, MigrateCommand
from extentions import bcrypt

def create_app():
    flask_app = Flask(__name__, instance_relative_config=True)
    AdminLTE(flask_app)

    config_name = os.getenv('FLASK_CONFIG', 'default')
    flask_app.config.from_object(config[config_name])
    flask_app.config.from_pyfile('app.cfg', silent=True)
    login_manager.session_protection = 'AdminPassword4Me'
    login_manager.login_view = 'signin'
    login_manager.login_message = 'Unauthorized User.'
    login_manager.login_message_category = "info"
    login_manager.init_app(flask_app)
    flask_app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///example.db'
    flask_app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
    db.init_app(flask_app)

    with flask_app.app_context():
        from models import User
        db.create_all()
        #db.session.merge(User(id=1,email='anjing@cuc.edu.cn',username='anjing',_password='123456'))
        
        db.session.merge(User(id=1,email='anjing@cuc.edu.cn',username='anjing',_password=generate_password_hash('123456')))
        db.session.commit()
        bcrypt.init_app(flask_app)

    for bp in all_blueprints:
        import_module(bp.import_name)
        flask_app.register_blueprint(bp)

    return flask_app

if __name__ == "__main__":
    flask_app=create_app()
    flask_app.run(host='0.0.0.0', port=5000, debug=True)