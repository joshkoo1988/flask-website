from koobyte import app, limiter
from flask import  redirect, url_for, render_template, send_from_directory
from flask import request
from flask_login import login_required, logout_user
from models import *


@app.route('/')
@limiter.limit("10 per minute")
def home():
    try:
        recent_posts = Post.query.order_by(Post.created.desc()).limit(3).all()
        if not recent_posts:
            app.logger.warning("No recent posts found")
    except Exception as e:
        app.logger.error(f"Error querying recent posts: {e}")
        recent_posts = []
    return render_template('home.html', recent_posts=recent_posts)

@app.route('/about')
@limiter.limit("10 per minute")
def about():
    return render_template('about.html')

@app.route('/timeline')
@limiter.limit("10 per minute")
def timeline():
    try:
        timeline_events = TimelineEvent.query.order_by(TimelineEvent.date.desc()).all()
        if not timeline_events:
            app.logger.warning("No timeline events found")
    except Exception as e:
        app.logger.error(f"Error querying timeline events: {e}")
        timeline_events = []
    return render_template('timeline.html', timeline_events=timeline_events)

@app.route('/login')
@limiter.limit("5 per minute")
def login():
    return redirect(url_for('security.login', next=request.url))

@app.route('/logout')
@limiter.limit("5 per minute")
@login_required
def logout():
    logout_user()
    return redirect(url_for('home'))

@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404

@app.errorhandler(500)
def internal_server_error(e):
    return render_template('500.html'), 500

@app.route('/robots.txt')
def robots_txt():
    return send_from_directory(app.root_path, 'robots.txt')