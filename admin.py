from flask import redirect, url_for, request
from flask_admin import Admin, BaseView, expose, AdminIndexView
from flask_admin.contrib.sqla import ModelView
from flask_security import current_user
from models import db, Post, Tag, generate_slug, TimelineEvent
from koobyte import app


class AdminMixin:
    def is_accessible(self):
        return current_user.is_authenticated and current_user.has_role('admin')

    def inaccessible_callback(self, name,**kwargs):
        return redirect(url_for('security.login', next=request.url))


class AdminView(AdminMixin, ModelView):
    pass


class HomeAdminView(AdminMixin, AdminIndexView):
    pass


class BaseModelView(ModelView):
    def on_model_change(self, form, model, is_created):
        if is_created:
            model.slug = generate_slug(model)
            db.session.add(model)
            db.session.commit()
        return super().on_model_change(form, model, is_created)
    
class PostAdminView(AdminMixin, BaseModelView):
    form_columns = ['title', 'body', 'tags']

class TagAdminView(AdminMixin, BaseModelView):
    form_columns = ['title']
    
class TimelineEventAdminView(AdminMixin, BaseModelView):
    form_columns = ['event', 'date']
    
    def on_model_change(self, form, model, is_created):
        # Override to avoid generating slug for TimelineEvent
        return super(BaseModelView, self).on_model_change(form, model, is_created)

admin = Admin(app, name='KooBytes', url='/',index_view=HomeAdminView(name='Home'))


def init_admin(app):
    admin.add_view(PostAdminView(Post, db.session))
    admin.add_view(TagAdminView(Tag, db.session))
    admin.add_view(TimelineEventAdminView(TimelineEvent, db.session))

