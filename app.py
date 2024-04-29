from flask import Flask, render_template, request, redirect, session, url_for
import sqlite3
import os

app = Flask(__name__)
app.secret_key = os.urandom(24)  # Secret key for session management

# Function to create a connection to the SQLite database
def get_db_connection():
    conn = sqlite3.connect('amit.db')
    conn.row_factory = sqlite3.Row
    return conn

# Function to create a new SQLite database table
def create_new_db_table(cursor):
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            email TEXT NOT NULL,
            password TEXT NOT NULL
        )
    ''')

# Route for the homepage
@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        # If the form submitted is for signup
        if 'signup' in request.form:
            email = request.form['email']
            password = request.form['password']
            
            # Insert user data into the database
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute('INSERT INTO users (email, password) VALUES (?, ?)', (email, password))
            conn.commit()
            cursor.close()
            conn.close()
            
            return 'Signup successful. Please login.'
        
        # If the form submitted is for login
        elif 'login' in request.form:
            email = request.form['email']
            password = request.form['password']
            
            # Query the database to check if the user exists
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute('SELECT * FROM users WHERE email = ? AND password = ?', (email, password))
            user = cursor.fetchone()
            conn.close()
            
            if user:
                # If user exists, store their email in session for authentication
                session['email'] = user['email']
                return redirect(url_for('dashboard'))  # Redirect to dashboard page
            else:
                return 'Invalid email or password'  # Display error message
    
    return render_template('index.html')

# Route for the dashboard
@app.route('/dashboard')
def dashboard():
    if 'email' in session:
        return f'Welcome, {session["email"]}! You are logged in.'  # Display welcome message
    else:
        return redirect(url_for('index'))  # Redirect to homepage if not logged in

if __name__ == '__main__':
    # Create the database file if it doesn't exist and establish the table
    conn = get_db_connection()
    create_new_db_table(conn.cursor())
    conn.close()
    
    app.run(debug=True)
