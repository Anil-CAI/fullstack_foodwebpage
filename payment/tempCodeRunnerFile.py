from flask import Flask, render_template, request, redirect, url_for, flash
import sqlite3

app = Flask(__name__, template_folder='templates')
app.secret_key = 'your_secret_key'  # Needed for flashing messages

DB_PATH = r'D:\Workspace\maha_rest\database\maha_rest.db'

def get_db_connection():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

@app.route('/', methods=['GET', 'POST'])
def payment():
    conn = get_db_connection()
    cart_items = conn.execute("SELECT id, fooditem, price, restaurant_name FROM cart").fetchall()
    conn.close()

    total = sum(item['price'] for item in cart_items)
    discounted = None
    coupon_code = request.form.get('coupon')

    # Detect which button was pressed by checking the submitted form
    if request.method == 'POST':
        if 'coupon' in request.form and coupon_code:
            # Apply coupon logic
            if coupon_code.lower() == 'food10':
                discount = 0.10 * total
            elif coupon_code.lower() == 'biryani50':
                discount = 50
            elif coupon_code.lower() == 'maha25':
                discount = 0.25 * total
            else:
                discount = 0
            discounted = max(total - discount, 0)
        elif 'payment_method' in request.form:
            # This means "Place Order" was clicked
            # Just flash the message and do not process order yet
            flash("Web page still under development so try again.. Thank you")

    return render_template('payment.html', cart=cart_items, total=total, discounted=discounted)

@app.route('/remove_item', methods=['POST'])
def remove_item():
    item_id = request.form.get('item_id')
    if item_id:
        conn = get_db_connection()
        conn.execute('DELETE FROM cart WHERE id = ?', (item_id,))
        conn.commit()
        conn.close()
    return redirect(url_for('payment'))

if __name__ == '__main__':
    app.run(debug=True)
