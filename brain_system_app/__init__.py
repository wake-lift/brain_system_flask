from flask import Flask
from flask_debugtoolbar import DebugToolbarExtension
from flask_simple_captcha import CAPTCHA
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from settings import Config, CAPTCHA_CONFIG

app = Flask(__name__)
app.config.from_object(Config)

engine = create_engine(Config.SQLALCHEMY_DATABASE_URI, echo=True)
session_factory = sessionmaker(engine)

toolbar = DebugToolbarExtension(app)

simple_captcha = CAPTCHA(config=CAPTCHA_CONFIG)
app = simple_captcha.init_app(app)


from . import error_handlers, forms, views  # noqa
