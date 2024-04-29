from flask import Flask, render_template, request, redirect
import mysql.connector
import os

app = Flask(__name__)

# Function to create a connection to the MySQL database
def get_db_connection():
    return mysql.connector.connect(
        host='localhost',
        user='root',
        password='1234',
        database='your_database'
    )

# Function to create a new MySQL database table
def create_new_db_table(cursor):
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INT AUTO_INCREMENT PRIMARY KEY,
            email VARCHAR(255) NOT NULL,
            password VARCHAR(255) NOT NULL
        )
    ''')

# Route for the homepage
@app.route('/')
def index():
    return render_template('index.html')

# Route to handle signup form submission
@app.route('/signup', methods=['POST'])
def signup():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        
        # Insert user data into the database
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('INSERT INTO users (email, password) VALUES (%s, %s)', (email, password))
        conn.commit()
        cursor.close()
        conn.close()
        
        return 'Data saved successfully.'

if __name__ == '__main__':
    app.run(debug=True)
