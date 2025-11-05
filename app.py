
from flask import Flask, render_template, request
import sqlite3
import datetime

app = Flask(__name__)
DB = 'orders.db'

# Initialize DB
conn = sqlite3.connect(DB)
c = conn.cursor()
c.execute("CREATE TABLE IF NOT EXISTS orders (id INTEGER PRIMARY KEY AUTOINCREMENT, vin TEXT, product TEXT, price REAL, start_date TEXT)")
conn.commit()
conn.close()

products = [
    {'name': 'CT Basic', 'min_price': 100, 'max_price': 200},
    {'name': 'CT Premium', 'min_price': 200, 'max_price': 400}
]

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/order', methods=['GET', 'POST'])
def order():
    if request.method == 'POST':
        vin = request.form['vin']
        product = request.form['product']
        price = float(request.form['price'])
        start_date = datetime.date.today().isoformat()

        selected = next((p for p in products if p['name'] == product), None)
        if selected and selected['min_price'] <= price <= selected['max_price']:
            conn = sqlite3.connect(DB)
            c = conn.cursor()
            c.execute('INSERT INTO orders (vin, product, price, start_date) VALUES (?, ?, ?, ?)', (vin, product, price, start_date))
            conn.commit()
            conn.close()
            return render_template('agreement.html', vin=vin, product=product, price=price, start_date=start_date)
        else:
            return 'Price out of range!'
    return render_template('order.html', products=products)

@app.route('/cancel', methods=['GET', 'POST'])
def cancel():
    if request.method == 'POST':
        order_id = request.form['order_id']
        conn = sqlite3.connect(DB)
        c = conn.cursor()
        c.execute('SELECT * FROM orders WHERE id=?', (order_id,))
        order = c.fetchone()
        conn.close()
        if order:
            refund = order[3] * 0.5  # Mock refund calculation
            return render_template('cancel_result.html', order=order, refund=refund)
        else:
            return 'Order not found!'
    return render_template('cancel.html')

if __name__ == '__main__':
    app.run(debug=True)
