import sqlite3
import os
import sys
import time
import bcrypt
from flask import Flask, render_template, request, redirect, url_for, session, flash

# App setup
app = Flask(__name__)
app.secret_key = os.environ.get("SECRET_KEY", "dev-secret-change-me")
DB_PATH = os.path.join(os.path.dirname(__file__), "users.db")

# Lockout policy
MAX_FAILED_ATTEMPTS = 3
LOCKOUT_SECONDS = 3
GENERIC_LOGIN_ERROR = "Invalid username or password"

# Password hashing (bcrypt)

def hash_password(password):
    return bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt()).decode("utf-8")

def verify_password(password, stored_hash):
    return bcrypt.checkpw(password.encode("utf-8"), stored_hash.encode("utf-8"))

# Dummy hash to check against when the username doesn't exist so
# "unknown user" takes about as long as long as "wrong password"
DUMMY_HASH = hash_password("not-a-real-password")

# Database creation

def get_db():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    conn = get_db() 
    conn.execute(
    """
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,  
        username TEXT UNIQUE NOT NULL,
        password_hash TEXT NOT NULL,
        failed_attempts INTEGER NOT NULL DEFAULT 0,
        locked_until REAL NOT NULL DEFAULT 0
    )
    """
    )
    conn.commit()
    conn.close()
    
# Browser routes

@app.route("/") # Entry point
def home():
    if "username" in session:
        return redirect(url_for("dashboard"))
    return redirect(url_for("login"))

@app.route("/register", methods=["GET", "POST"]) # Register user
def register():
    if request.method == "POST":
        username = request.form.get("username", "").strip()
        password = request.form.get("password", "")
        confirm = request.form.get("confirm_password", "")
        
        # Validation
        if not username or not password:
            flash("All fields are required.")
            return redirect(url_for("register"))
        
        if password != confirm:
            flash("Passwords do not match.")
            return redirect(url_for("register"))
        
        if len(password) < 8:
            flash("Password must be at least 8 characters long.")
            return redirect(url_for("register"))
        
        conn = get_db()
        existing = conn.execute(
            "SELECT id FROM users WHERE username = ?", (username,)
        ).fetchone()
        if existing:
            conn.close()
            flash("That username is already taken.")
            return redirect(url_for("register"))
        
        conn.execute(
            "INSERT INTO users (username, password_hash) "
            "VALUES (?, ?)", (username, hash_password(password)),
        )
        conn.commit()
        conn.close()
        
        flash("Account created successfully, Please log in.")
        return redirect(url_for("login"))
    
    return render_template("register.html")

@app.route("/login", methods=["GET", "POST"]) # Login user
def login():
    if request.method == "POST":
        username = request.form.get("username", "").strip()
        password = request.form.get("password", "")
        
        conn = get_db()
        user = conn.execute(
            "SELECT * FROM users WHERE username = ?", (username,)
        ).fetchone()
        
        if user is None:
            verify_password(password, DUMMY_HASH)
            conn.close()
            flash(GENERIC_LOGIN_ERROR)
            return redirect(url_for("login"))
        
        now = time.time()
        if user["locked_until"] > now:
            conn.close()
            minutes_left = int((user["locked_until"] - now) // 60) + 1
            flash("Too many failed login attempts. This account is temporarily "
                  f"locked. Try again in about {minutes_left} minute(s).")
            return redirect(url_for("login"))
        
        if verify_password(password, user["password_hash"]):
            conn.execute(
                "UPDATE users SET failed_attempts = 0, locked_until = 0 WHERE id = ?",
                (user["id"],),
            )
            conn.commit()
            conn.close()
            session["username"] = username
            flash("Logged in successfully.")
            return redirect(url_for("dashboard"))
        
        attempts = user["failed_attempts"]
        if user["locked_until"] != 0:
            attempts = 0
        attempts += 1
        
        if attempts >= MAX_FAILED_ATTEMPTS:
            conn.execute(
                "UPDATE users SET failed_attempts = ?, locked_until = ? WHERE id = ?",
                (attempts, now + LOCKOUT_SECONDS, user["id"]),
            )
            conn.commit()
            conn.close()
            flash("Too many failed login attempts. This account is temporarily "
                  f"locked for {LOCKOUT_SECONDS} seconds")
            return redirect(url_for("login"))
        
        conn.execute(
            "UPDATE users SET failed_attempts = ?, locked_until = 0 WHERE id = ?",
            (attempts, user["id"]),
        )
        conn.commit()
        conn.close()
        flash(GENERIC_LOGIN_ERROR)
        return redirect(url_for("login"))
    
    return render_template("login.html")

@app.route("/logout") # User logout
def logout():
    session.pop("username", None)
    flash("You have been logged out.")
    return redirect(url_for("login"))

@app.route("/dashboard") # User dashboard
def dashboard():
    if "username" not in session:
        flash("Please log in first,")
        return redirect(url_for("login"))
    return render_template("dashboard.html", username=session["username"])

@app.route("/reset", methods=["GET", "POST"]) # User password rest
def reset_password():
    """Reset a password: enter a username and a new password."""
    if request.method == "POST":
        username = request.form.get("username", "").strip()
        new_password = request.form.get("new_password", "")
        confirm = request.form.get("confirm_password", "")
        
        conn = get_db()
        user = conn.execute(
            "SELECT * FROM users WHERE username = ?", (username,)
        ).fetchone()
        
        # Validation
        if not user:
            conn.close()
            flash("Account not found")
            return redirect(url_for("reset_password"))
        
        if new_password != confirm:
            conn.close()
            flash("Passwords do not match.")
            return redirect(url_for("reset_password"))
        
        conn.execute(
            "UPDATE users SET password_hash = ? WHERE username = ?",
            (hash_password(new_password), username),
        )
        conn.commit()
        conn.close()
        flash("Password reset succcessfully. Please log in.")
        return redirect(url_for("login"))

    return render_template("reset_password.html")
    
# Program start
if __name__ == "__main__":
    init_db()
    app.run(debug=True)
