from flask import Blueprint, render_template, request, flash, current_app as app
from flask import redirect, url_for
from models import *
from .forms import PostForm
from flask_security import login_required
from sqlalchemy.orm import joinedload
from flask_wtf import CSRFProtect

csrf = CSRFProtect()

posts = Blueprint('posts', __name__, template_folder='templates')

@posts.route('/create', methods=['GET', 'POST'])
@login_required
@csrf.exempt
def create_post():
    form = PostForm()
    if request.method == 'POST':
        title = request.form.get('title')
        body = request.form.get('body')
        try:
            post = Post(title=title, body=body)
            db.session.add(post)
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            flash('An error occurred while creating the post.', 'danger')
            app.logger.error(f'Error creating post: {e}')
    return render_template('posts/post_create.html', form=form)

@posts.route('/')
def posts_list():
    q = request.args.get('q')
    if q:
        query = Post.query.options(joinedload(Post.tags)).filter(
            (Post.title.contains(q)) |
            (Post.body.contains(q)) |
            (Tag.title.contains(q))
        ).join(Post.tags)
    else:
        query = Post.query.order_by(Post.created.desc())

    page = request.args.get('page', 1, type=int)
    pages = query.paginate(page=page, per_page=3)

    return render_template('posts/posts.html', pages=pages, q=q)

@posts.route('/<slug>')
def post_detail(slug):
    post = Post.query.filter(Post.slug == slug).first()
    return render_template('posts/post_detail.html', post=post)

@posts.route('/tags/<slug>')
def tag_detail(slug):
    tag = Tag.query.filter(Tag.slug == slug).first()
    return render_template('posts/tag_detail.html', tag=tag)

@posts.route('/<slug>/edit', methods=['GET', 'POST'])
@login_required
def post_update(slug):
    post = Post.query.filter(Post.slug == slug).first()
    if request.method == 'POST':
        form = PostForm(formdata=request.form, obj=post)
        form.populate_obj(post)
        db.session.commit()
        return redirect(url_for('posts.post_detail', slug=post.slug))
    form = PostForm(obj=post)
    return render_template('posts/edit.html', form=form, post=post)