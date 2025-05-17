from flask import Flask, redirect, url_for, request
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_admin import Admin
from config import Config
from flask_admin.contrib.sqla import ModelView
from flask_security import SQLAlchemyUserDatastore, Security, current_user
from flask_security.decorators import roles_required
from flask_wtf import CSRFProtect
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from redis import Redis
from flask_talisman import Talisman

app = Flask(__name__)
app.config.from_object(Config)
db =SQLAlchemy(app)
migrate = Migrate(app, db)

csrf = CSRFProtect(app)

redis_store = Redis(host='localhost', port=6379, db=0)

limiter = Limiter(
    get_remote_address,
    app=app,
    storage_uri="redis://localhost:6379"
)

csp = {
    'default-src': [
        '\'self\'',
        'https://trusted.cdn.com'
    ],
    
    'script-src': [
        '\'self\'',
        'https://trusted.cdn.com',
        'https://stackpath.bootstrapcdn.com',
        'https://cdn.jsdelivr.net',
        'https://cdnjs.cloudflare.com',
        'https://kit.fontawesome.com'
    ],

    'style-src': [
        '\'self\'',
        'https://trusted.cdn.com',
        'https://stackpath.bootstrapcdn.com',
        'https://cdn.jsdelivr.net',
        'https://cdnjs.cloudflare.com', 
        'https://kit.fontawesome.com',
        '\'unsafe-inline\''
    ],

    'style-src-elem': [
        "'self'",
        'https://trusted.cdn.com',
        'https://stackpath.bootstrapcdn.com',
        'https://cdn.jsdelivr.net',
        'https://cdnjs.cloudflare.com',
        'https://kit.fontawesome.com',
        'https://fonts.googleapis.com'
    ],

    'font-src': [
        "'self'",
        'https://trusted.cdn.com',
        'https://cdnjs.cloudflare.com',   
        'https://kit.fontawesome.com',
        'https://fonts.gstatic.com'
    ],

    'img-src': [
        '\'self\'',
        'data:', 
        'https://trusted.cdn.com'
    ]
}

talisman = Talisman(app, content_security_policy=csp, force_https=True)

from models import *
from admin import *
from views import *
from posts.blueprint import posts

init_admin(app)

user_datastore = SQLAlchemyUserDatastore(db, User, Role)
security = Security(app, user_datastore)

app.register_blueprint(posts, url_prefix='/blog')

