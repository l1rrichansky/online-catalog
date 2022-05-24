from wtforms import Form, StringField, TextAreaField, IntegerField, SelectField, SubmitField
from flask_wtf import FlaskForm
from wtforms.validators import *


class ItemForm(Form):
    name = StringField('Имя товара')
    body = TextAreaField('Описание')
    price = StringField('Стоимость в рублях')


class OrderForm(Form):
    email = StringField("Email: ", validators=[data_required(), Email()])
    ph_num = IntegerField("Телефон: ", validators=[data_required(), Length(min=9, max=13)])
    submit = SubmitField("Отправить")
