import os

from flask import Flask
from flask_debugtoolbar import DebugToolbarExtension
from flask_simple_captcha import CAPTCHA
# from flask_migrate import Migrate
# from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker

from settings import Config, CAPTCHA_CONFIG
# from .models import BoughtInProduct, BoughtInProductAsAPartOf, BoughtInProductLink

app = Flask(__name__)
app.config.from_object(Config)

engine = create_engine(Config.SQLALCHEMY_DATABASE_URI, echo=True)
# session = Session(engine)
session_factory = sessionmaker(engine)

toolbar = DebugToolbarExtension(app)

simple_captcha = CAPTCHA(config=CAPTCHA_CONFIG)
app = simple_captcha.init_app(app)
# db = SQLAlchemy(app)


from . import error_handlers, forms, views # noqa

# migrate = Migrate(app, db)
