from koobyte import db, app
from models import Post, Tag

with app.app_context():
    # Create a new post
    new_post = Post(title="another test post", body="another test post")
    new_tag = Tag(title="test2", slug="test2")

    # Add the new post to the session
    db.session.add(new_post)
    db.session.add(new_tag)

    # Commit the session to save the post to the database
    db.session.commit()

    print("New post created with id:", new_post.id)
    print("New post slug:", new_post.slug)
    print("New tag created with id:", new_tag.id)
    print("New tag slug:", new_tag.slug)