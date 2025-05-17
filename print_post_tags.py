from koobyte import db, app
from models import Post, Tag

with app.app_context():
    all_tags = Tag.query.all()
    for tag in all_tags:
        print(f'Tag id: {tag.id}, slug: {tag.slug}')

    all_posts = Post.query.all()
    for post in all_posts:
        print(f'Post id: {post.id}, slug: {post.slug}')
