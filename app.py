import datetime

from flask import Flask
from config import Configuration
from flask_sqlalchemy import SQLAlchemy
from flask import request, redirect, url_for, session

from flask_migrate import Migrate
from flask_security import SQLAlchemyUserDatastore, Security

from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView
from flask_admin import AdminIndexView

from flask_security import current_user

app = Flask(__name__)
app.config.from_object(Configuration)
app.permanent_session_lifetime = datetime.timedelta(days=1)


db = SQLAlchemy(app)
migrate = Migrate(app, db)


from models import *


class AdminMixin:
    def is_accessible(self):
        return current_user.has_role('admin')

    def inaccessible_callback(self, name, **kwargs):
        return redirect(url_for('security.login', next=request.url))


class BaseModelView(ModelView):
    def on_model_change(self, form, model, is_created):
        model.generate_slug()
        return super(BaseModelView, self).on_model_change(form, model, is_created)


class AdminView(AdminMixin, ModelView):
    pass


class HomeAdminView(AdminMixin, AdminIndexView):
    pass


class ItemAdminView(AdminMixin, BaseModelView):
    column_labels = dict(body='Description', isActive='isActive')
    column_list = ['id', 'name', 'body', 'price', 'isActive']
    form_columns = ['name', 'body', 'price', 'isActive', 'img_url']


class OrderAdminView(AdminMixin, ModelView):
    column_labels = dict(del_met='Delivery method', pay_met='Payment method', id='Number')
    column_list = ['id', 'items', 'price', 'client_name', 'client_surname', 'email', 'note', 'phone_number', 'del_met', 'pay_met', 'status']


admin = Admin(app, 'AdminPanel', url='/', index_view=HomeAdminView())
admin.add_view(ItemAdminView(Item, db.session))
admin.add_view(OrderAdminView(Order, db.session))



user_datastore = SQLAlchemyUserDatastore(db, User, Role)
security = Security(app, user_datastore)

