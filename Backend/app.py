from flask import Flask, render_template, request, redirect, session, url_for, flash
from flask_socketio import SocketIO, emit
from flask_mysqldb import MySQL
from dotenv import load_dotenv
import os
import random

load_dotenv()

app = Flask(
    __name__,
    template_folder="../Frontend/templates", # Folder direction to templates and static
    static_folder="../Frontend/static"
)

#socketio connection
socketio = SocketIO(app, cors_allowed_origins="*")
app.secret_key = os.getenv("SECRET_KEY", "secret!")

# MySQL configuration
app.config['MYSQL_HOST'] = os.getenv("HOST")
app.config['MYSQL_USER'] = os.getenv("USER")
app.config['MYSQL_PASSWORD'] = os.getenv("PASSWORD")
app.config['MYSQL_DB'] = os.getenv("DATABASE")

# mysql and Advanced encrytion seceruty (AES) connections
mysql = MySQL(app)
AES_KEY = os.getenv("AES_KEY")

# 2 Arrys room and connected players witch will store data
rooms = {}
connected_players = {}


# Main rought to home page where you need to be logged in
@app.route("/")
def home():
    if 'user_id' not in session:
        flash("You must be logged in to view this page!")
        return redirect(url_for('login'))
    return render_template("index.html", username=session.get('username'))



# Register page and countinues if form is accepted
@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']
        confirm_password = request.form['confirm_password']

        if password != confirm_password:
            flash("Passwords do not match. Please try again.")
            return render_template('register.html')

        cur = mysql.connection.cursor()
        cur.execute("""
            INSERT INTO user (username, email, password)
            VALUES (%s, %s, AES_ENCRYPT(%s, %s))
        """, (username, email, password, AES_KEY))
        mysql.connection.commit()
        cur.close()

        flash("Registration successful! Please log in.")
        return redirect(url_for('login'))

    return render_template('register.html')



# Page for Login were its a form that collects data and matches data with data
@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form['username']
        password = request.form['password']

        cur = mysql.connection.cursor()
        cur.execute("""
            SELECT id, username, AES_DECRYPT(password, %s)
            FROM user
            WHERE username = %s
        """, (AES_KEY, username))
        user = cur.fetchone()
        cur.close()

        if user and user[2].decode('utf-8') == password:
            session['user_id'] = user[0]
            session['username'] = user[1]
            flash("Login successful!")
            return redirect(url_for('home'))
        else:
            flash("Invalid credentials. Please try again.")

    return render_template('login.html')


@app.route("/logout")
def logout():
    session.clear()
    flash("You have been logged out!")
    return redirect(url_for('home'))


@socketio.on("new_message")
def handle_new_message(user_message):
    print(f"{user_message}")
    emit("chat", {"user_message": user_message["user_message"]}, broadcast=True)

if __name__ == "__main__":
    socketio.run(app, debug=True, port=7500)