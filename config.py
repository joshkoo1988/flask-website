import os
from dotenv import load_dotenv

load_dotenv()

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

class Config:
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(BASE_DIR, 'koobytes.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = os.environ.get('SECRET_KEY')
    if not SECRET_KEY:
        raise ValueError("SECRET_KEY is not set.")
    SECURITY_PASSWORD_SALT = os.environ.get('SECURITY_PASSWORD_SALT')
    if not SECURITY_PASSWORD_SALT:
        raise ValueError("SECURITY_PASSWORD_SALT is not set.")
    SECURITY_PASSWORD_HASH = 'sha512_crypt'
    SECURITY_URL_PREFIX = "/auth"
    SECURITY_LOGIN_URL = "/auth/login"
    SECURITY_LOGOUT_URL = "/auth/logout"
    SECURITY_POST_LOGIN_VIEW = "/admin"
    SECURITY_POST_LOGOUT_VIEW = "/"
    SECURITY_USE_SSL = True

    SESSION_COOKIE_NAME = 'test'  # Customize your session cookie name
    SESSION_COOKIE_HTTPONLY = True  # Protect from XSS
    SESSION_COOKIE_SAMESITE = 'Lax'  # Helps with CSRF protection