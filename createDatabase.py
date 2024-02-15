from flask import Flask, render_template, request, redirect, url_for
import sqlite3

app = Flask(__name__)

# Database setup
def create_table():
    conn = sqlite3.connect('receipts.db')
    c = conn.cursor()

    # Print the SQL statement used for creating the table
    create_table_sql = '''CREATE TABLE IF NOT EXISTS receipts
                          (id INTEGER PRIMARY KEY, date TEXT, time TEXT, liters REAL, total_dollar REAL, vehicle TEXT, odometer INTEGER, fuel_card TEXT, payment_method TEXT)'''
    print("Creating table with SQL statement:")
    print(create_table_sql)

    # Execute the SQL statement to create the table
    c.execute(create_table_sql)

    # Print the table schema to verify its structure
    c.execute("PRAGMA table_info(receipts)")
    print("Table schema after creation:")
    print(c.fetchall())

    conn.commit()
    conn.close()

# Route for home page
@app.route('/')
def home():
    return render_template('index.html')

# Route for submitting the form
@app.route('/submit', methods=['POST'])
def submit():
    date = request.form['date']
    time = request.form['time']
    liters = request.form['liters']
    total_dollar = request.form['total_dollar']
    vehicle = request.form['vehicle']
    odometer = request.form['odometer']
    fuel_card = request.form['fuel_card']
    payment_method = request.form['payment_method']

    conn = sqlite3.connect('receipts.db')
    c = conn.cursor()
    c.execute("INSERT INTO receipts (date, time, liters, total_dollar, vehicle, odometer, fuel_card, payment_method) VALUES (?, ?, ?, ?, ?, ?, ?, ?)",
              (date, time, liters, total_dollar, vehicle, odometer, fuel_card, payment_method))
    conn.commit()
    conn.close()

    return redirect(url_for('home'))

# Route for querying data
@app.route('/query')
def query():
    conn = sqlite3.connect('receipts.db')
    c = conn.cursor()
    c.execute("SELECT * FROM receipts")
    data = c.fetchall()
    conn.close()
    return render_template('query.html', data=data)

if __name__ == '__main__':
    create_table()
    app.run(debug=True)
