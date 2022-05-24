from .forms import ItemForm, OrderForm
from models import Item, Order
import mysql.connector
from app import db, app
from flask_security import login_required
from flask import redirect, url_for, request, session, render_template, Blueprint, flash


items = Blueprint('items', __name__, template_folder='templates')


@items.route('/')
def index():
    items = Item.query.all()
    return render_template('items/index.html', items=items)


@items.route('/create', methods=['POST', 'GET'])
@login_required
def create_item():
    if request.method == "POST":
        name = request.form['name']
        body = request.form['body']
        price = request.form['price']
        try:
            item = Item(name=name, body=body, price=price)
            db.session.add(item)
            db.session.commit()
        except:
            print('Добавить товар не удалось')
        return redirect(url_for('items.index'))
    form = ItemForm()
    return render_template('items/create_item.html', form=form)


@items.route('/search')
def search():
    q = request.args.get('q')
    if q:
        searched_items = Item.query.filter(Item.name.contains(q) | Item.body.contains(q)).all()
    else:
        searched_items = Item.query.all()
    return render_template('items/search.html', items=searched_items, q=q)


@app.route('/checkout', methods=['GET', 'POST'])
def checkout():
    if 'cart' in session:
        pass
    else:
        session['cart'] = []


    if request.method == "POST":
        items = Item.query.all()
        price = summing(items)
        cl_name = request.form['cl_name']
        cl_surname = request.form['cl_surname']
        email = request.form['email']
        ph_num = request.form['ph_num']
        del_met = request.form['del_met']
        pay_met = request.form['pay_met']
        address = request.form['address']
        note = request.form['note']
        item_list = str()
        for i in session['cart']:
            item_list += str(str(i['item_name'])+'; Количество: ' + str(i['qty']) + '; Cтоимость: ' + str(i['item_price']) + ';                      \n')
        order = Order(client_name=cl_name,
                      client_surname=cl_surname,
                      phone_number=ph_num,
                      email=email,
                      del_met=del_met,
                      pay_met=pay_met,
                      mail_address=address,
                      price=price,
                      note=note,
                      items=item_list
                      )
        db.session.add(order)
        db.session.commit()
        session.pop('cart', None)
        return render_template('after_order.html', order_id=order.id)

    items = Item.query.all()
    sum = summing(items)
    return render_template('checkout.html', cl=session["cart"], lencl=len(session["cart"]), items=items, sum=sum)


def get_cart():
    item_list = []
    for item in session["cart"]:
        item_list.append(item['item_name'])
    return item_list


@app.route('/shopcart', methods=['GET', 'POST'])
def shopcart():
    if 'cart' in session:
        pass
    else:
        session['cart'] = []
    if request.method == 'POST':
        if request.form.get('plus_item'):
            temp_id = request.form['temp_id']
            for i in range(len(session['cart'])):
                print(temp_id)
                print(session['cart'][i]['item_id'])
                if int(session['cart'][i]['item_id']) == int(temp_id):
                    print('found')
                    session['cart'][i]['qty'] += 1
                    print(session['cart'])
        elif request.form.get('minus_item'):
            temp_id = request.form['temp_id']
            for i in range(len(session['cart'])):
                if int(session['cart'][i]['item_id']) == int(temp_id):
                    session['cart'][i]['qty'] -= 1
                    print(session['cart'])
        else:
            pass
    delete_id = int()
    check = 0
    if 'cart' in session:
        for i in range(len(session['cart'])):
            if int(session['cart'][i]['qty']) == 0:
                delete_id = i
                check = 1
        if check == 1:
            session['cart'].pop(delete_id)
        else:
            pass
    items = Item.query.all()
    sum = summing(items)
    return render_template('shopcart.html', items=items, cl=session["cart"], sum=sum)


def summing(inp):
    summ = 0
    for i in inp:
        for j in session["cart"]:
            if i.id == j['item_id']:
                summ += i.price * j['qty']
    return summ


@app.route('/delete')
def delete_visits():
    session.pop('cart', None)  # удаление данных о посещениях
    return redirect('/shopcart')


@items.route('/<slug>', methods=['GET', 'POST'])
def item_detail(slug):
    session.permanent = True
    item = Item.query.filter(Item.slug == slug).first_or_404()
    if request.method == 'POST':
        id = int(request.form['item_id'])
        item_name = request.form['item_name']
        item_price = request.form['item_price']
        qty = 1
        cart_session()
        matching = [d for d in session['cart'] if d['item_id'] == id]
        if matching:
            matching[0]['qty'] += qty
        else:
            session["cart"].append(dict({'item_id': id, 'qty': qty, 'item_name': item_name, 'item_price': item_price}))
        flash('Товар успешно добавлен в корзину')
    else:
        pass
    return render_template('items/item_detail.html', item=item)


def cart_session():
    if 'cart' in session:
        pass
    else:
        session['cart'] = []
