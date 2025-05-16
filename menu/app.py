from flask import Flask, render_template, jsonify, request, url_for
import sqlite3
import os

# Set correct paths
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
ROOT_DIR = os.path.dirname(BASE_DIR)
DB_PATH = os.path.join(ROOT_DIR, 'database', 'maha_rest.db')
STATIC_FOLDER = os.path.join(ROOT_DIR, 'static')

# Create the app
app = Flask(__name__, static_folder=STATIC_FOLDER, template_folder='templates')

def get_db_connection():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

@app.route('/')
def home():
    conn = get_db_connection()
    restaurants = conn.execute("SELECT id, name, location, rating FROM restaurants").fetchall()
    conn.close()
    return render_template('menu.html', restaurants=restaurants)

@app.route('/get_menu/<int:restaurant_id>')
def get_menu(restaurant_id):
    conn = get_db_connection()
    items = conn.execute("""
        SELECT name, description, price
        FROM food_items
        WHERE restaurant_id = ?
    """, (restaurant_id,)).fetchall()
    conn.close()
    return jsonify([dict(item) for item in items])

@app.route('/add_to_cart', methods=['POST'])
def add_to_cart():
    data = request.get_json()
    conn = get_db_connection()

    conn.execute("""
        CREATE TABLE IF NOT EXISTS cart (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            fooditem TEXT NOT NULL,
            price REAL NOT NULL,
            restaurant_name TEXT NOT NULL
        )
    """)
    conn.execute("""
        INSERT INTO cart (fooditem, price, restaurant_name)
        VALUES (?, ?, ?)
    """, (data['fooditem'], data['price'], data['restaurant_name']))

    conn.commit()
    conn.close()
    return jsonify({"status": "added to cart"})

if __name__ == '__main__':
    app.run(debug=True)
