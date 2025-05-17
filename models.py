from datetime import datetime
from time import time
import re
from koobyte import db
from flask_security import UserMixin, RoleMixin
import uuid
from sqlalchemy.ext.hybrid import hybrid_property
import markdown

def slugify(s):
    pattern = r'[^\w+]'
    return re.sub(pattern, '-', s)

def generate_slug(instance):
    if instance.title:
        return slugify(instance.title)
    else:
        return str(int(time()))


posts_tags = db.Table('posts_tags',
    db.Column('post_id', db.Integer, db.ForeignKey('post.id')),
    db.Column('tag_id', db.Integer, db.ForeignKey('tag.id'))
)

roles_users = db.Table('roles_users',
    db.Column('user_id', db.Integer, db.ForeignKey('user.id')),
    db.Column('role_id', db.Integer, db.ForeignKey('role.id'))         
)

class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(140))
    slug = db.Column(db.String(140), unique=True)
    body = db.Column(db.Text)
    created = db.Column(db.DateTime, default=datetime.now)
    tags = db.relationship('Tag', secondary=posts_tags, backref=db.backref('posts', lazy='dynamic'))

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.slug = generate_slug(self)

    def to_html(self):
        return markdown.markdown(self.body)
    
    def title_to_html(self):
        return markdown.markdown(self.title)

    def __repr__(self):
        return f'<Post id: {self.id}, title: {self.title}>'
    
class Tag(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(140))
    slug = db.Column(db.String(140), unique=True)\
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.slug = generate_slug(self)


    def __repr__(self):
        return f'<Tag id: {self.id}, title: {self.title}>'
    
class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(140), unique=True)
    password = db.Column(db.String(255))
    active = db.Column(db.Boolean)
    roles = db.relationship('Role', secondary='roles_users', backref=db.backref('users', lazy='dynamic'))
    _fs_uniquifier = db.Column('fs_uniquifier', db.String(255), unique=True, nullable=False, default=lambda: str(uuid.uuid4()))

    @hybrid_property
    def fs_uniquifier(self):
        return self._fs_uniquifier
    
    @fs_uniquifier.setter
    def fs_uniquifier(self, value):
        self._fs_uniquifier = value

class Role(db.Model, RoleMixin):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(140), unique=True)
    description = db.Column(db.String(255))

class TimelineEvent(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    event = db.Column(db.String(255), nullable=False)
    date = db.Column(db.Date, nullable=False)

    def __repr__(self):
        return f'<TimelineEvent {self.event}>'