import uuid
from flask import Flask, render_template, redirect, url_for, session, jsonify

app = Flask(__name__)
app.secret_key = 'simple-ecommerce-app'

products = [
    {'id': 1, 'name': 'Chair', 'image': 'chair.jpg', 'price': 2999},
    {'id': 2, 'name': 'Watch', 'image': 'watch.jpg', 'price': 5499},
    {'id': 3, 'name': 'Table', 'image': 'table.jpg', 'price': 3499},
    {'id': 4, 'name': 'Laptop', 'image': 'laptop.jpg', 'price': 59999},
    {'id': 5, 'name': 'Shirt', 'image': 'shirt.jpg', 'price': 1599},
]


def get_product_by_id(product_id):
    return next((p for p in products if p['id'] == product_id), None)

@app.route('/')
def index():
    session.pop('cart', None)
    return render_template('index.html', products=products)

@app.route('/add_to_cart/<int:product_id>')
def add_to_cart(product_id):
    if 'cart' not in session:
        session['cart'] = []

    product = get_product_by_id(product_id)
    if product and product not in session['cart']:
        session['cart'].append(product)

    return redirect(url_for('cart'))

@app.route('/cart')
def cart():
    cart_items = session.get('cart', [])
    grand_total = sum(item['price'] for item in cart_items) 
    return render_template('cart.html', cart_items=cart_items, grand_total=grand_total)


@app.route('/pay', methods=['POST'])
def pay_now():
    session.pop('cart', None)
    transaction_id = str(uuid.uuid4())
    return jsonify(message='Payment Successful', transaction_id=transaction_id)

@app.route('/clear_cart', methods=['POST'])
def clear_cart():
    session.pop('cart', None)
    return '', 204 

if __name__ == '__main__':
    app.run(debug=True)
