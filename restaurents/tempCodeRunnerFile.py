import os
from flask import Flask, render_template, jsonify
import sqlite3

# Define project root folder (one level above this file)
PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))

app = Flask(
    __name__,
    template_folder=os.path.join(PROJECT_ROOT, 'restaurants', 'template'),  # Your template folder
    static_folder=os.path.join(PROJECT_ROOT, 'static')                     # Your static folder
)

def connect_db():
    db_path = os.path.join(PROJECT_ROOT, 'database', 'maha_rest.db')
    if not os.path.exists(db_path):
        print("Database not found.")
        return None
    return sqlite3.connect(db_path)

def get_restaurants():
    conn = connect_db()
    if conn is None:
        return []
    cursor = conn.cursor()
    cursor.execute('SELECT name, location, rating FROM restaurants')
    data = cursor.fetchall()
    conn.close()

    return [{"name": row[0], "location": row[1], "rating": row[2]} for row in data]

@app.route('/')
def home():
    return render_template('restaurants.html')

@app.route('/api/restaurant')
def restaurant_api():
    restaurants = get_restaurants()
    return jsonify(restaurants)

if __name__ == '__main__':
    app.run(debug=True)
