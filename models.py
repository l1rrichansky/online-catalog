import sqlalchemy
from sqlalchemy import *
from flask_security import UserMixin, RoleMixin

from app import db
import re


def slugify(s):
    pattern = r'[^\w+]'
    return re.sub(pattern, '-', s)


class Item(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(140), unique=True, nullable=False)
    slug = db.Column(db.String(140), unique=True)
    body = db.Column(db.Text)
    price = db.Column(db.Integer)
    img_url = db.Column(db.String(140))
    isActive = db.Column(db.Boolean, default=True)

    def __init__(self, *args, **kwargs):
        super(Item, self).__init__(*args, **kwargs)
        self.generate_slug()

    def generate_slug(self):
        if self.name:
            self.slug = slugify(self.name)

    def __repr__(self):
        return self.name





class Order(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    client_name = db.Column(db.String(150))
    client_surname = db.Column(db.String(150))
    phone_number = db.Column(db.String(150), nullable=False)
    email = db.Column(db.String(150), nullable=False)
    del_met = db.Column(db.String(150))
    pay_met = db.Column(db.String(150))
    mail_address = db.Column(db.String(150))
    note = db.Column(db.String(150))
    price = db.Column(db.Integer)
    status = db.Column(db.String(150), default='Ожидает подтверждения')
    items = db.Column(db.String(1000))


roles_users = db.Table('roles_users',
                       db.Column('user_id', db.Integer(), db.ForeignKey('user.id')),
                       db.Column('role_id', db.Integer(), db.ForeignKey('role.id'))
                       )


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(255))
    active = db.Column(db.Boolean())
    roles = db.relationship('Role', secondary=roles_users, backref=db.backref('users', lazy='dynamic'))


class Role(db.Model, RoleMixin):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), unique=True, nullable=False)
    description = db.Column(db.String(255))
