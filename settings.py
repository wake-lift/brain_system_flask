import os
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent


class Config(object):
    SQLALCHEMY_DATABASE_URI = os.getenv('SQLALCHEMY_DATABASE_URI')
    SECRET_KEY = os.getenv('SECRET_KEY')
    UPLOAD_DIR = os.path.join(BASE_DIR, os.getenv('FLASK_APP'), 'media')


CAPTCHA_CONFIG = {
    'SECRET_CAPTCHA_KEY': os.getenv('SECRET_CAPTCHA_KEY'),
    'CAPTCHA_LENGTH': 6,
    'CAPTCHA_DIGITS': False,
    'BACKGROUND_COLOR': (255, 255, 255),
    'TEXT_COLOR': (0, 0, 0),
    'CAPTCHA_IMG_FORMAT': 'JPEG',
    'EXPIRE_SECONDS': 60 * 5,
}
