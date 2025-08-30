from flask import Flask, render_template, request, redirect, url_for, session, flash
import sqlite3
import os

app = Flask(__name__)
app.secret_key = "supersecret123"  # Change this for security

# ---------- DATABASE SETUP ----------
def init_db():
    conn = sqlite3.connect("database.db")
    cursor = conn.cursor()

    # Users table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL,
            role TEXT NOT NULL CHECK(role IN ('admin', 'user'))
        )
    ''')

    # Tickets table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS tickets (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            description TEXT NOT NULL,
            category TEXT,
            priority TEXT CHECK(priority IN ('Low', 'Medium', 'High')),
            status TEXT DEFAULT 'Open',
            user_id INTEGER,
            FOREIGN KEY(user_id) REFERENCES users(id)
        )
    ''')

    conn.commit()
    conn.close()

# Initialize DB if not exists
if not os.path.exists("database.db"):
    init_db()

# ---------- ROUTES ----------
@app.route("/")
def home():
    return redirect(url_for("login"))

@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        role = request.form["role"]

        conn = sqlite3.connect("database.db")
        cursor = conn.cursor()

        try:
            cursor.execute("INSERT INTO users (username, password, role) VALUES (?, ?, ?)", 
                           (username, password, role))
            conn.commit()
            flash("Registration successful! Please log in.", "success")
            return redirect(url_for("login"))
        except:
            flash("Username already exists!", "danger")
        finally:
            conn.close()
    return render_template("register.html")

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        conn = sqlite3.connect("database.db")
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM users WHERE username=? AND password=?", (username, password))
        user = cursor.fetchone()
        conn.close()

        if user:
            session["user_id"] = user[0]
            session["username"] = user[1]
            session["role"] = user[3]
            return redirect(url_for("dashboard"))
        else:
            flash("Invalid username or password!", "danger")
    return render_template("login.html")

@app.route("/dashboard")
def dashboard():
    if "user_id" not in session:
        return redirect(url_for("login"))

    conn = sqlite3.connect("database.db")
    cursor = conn.cursor()

    if session["role"] == "admin":
        cursor.execute("SELECT * FROM tickets")
        tickets = cursor.fetchall()
        cursor.execute("SELECT status, COUNT(*) FROM tickets GROUP BY status")
        stats = dict(cursor.fetchall())
    else:
        cursor.execute("SELECT * FROM tickets WHERE user_id=?", (session["user_id"],))
        tickets = cursor.fetchall()
        cursor.execute("SELECT status, COUNT(*) FROM tickets WHERE user_id=? GROUP BY status", (session["user_id"],))
        stats = dict(cursor.fetchall())

    conn.close()
    return render_template("dashboard.html", tickets=tickets, role=session["role"], stats=stats)

@app.route("/tickets/new", methods=["GET", "POST"])
def new_ticket():
    if "user_id" not in session:
        return redirect(url_for("login"))

    if request.method == "POST":
        title = request.form["title"]
        description = request.form["description"]
        category = request.form["category"]
        priority = request.form["priority"]

        conn = sqlite3.connect("database.db")
        cursor = conn.cursor()
        cursor.execute("INSERT INTO tickets (title, description, category, priority, user_id) VALUES (?, ?, ?, ?, ?)",
                       (title, description, category, priority, session["user_id"]))
        conn.commit()
        conn.close()
        flash("Ticket created successfully!", "success")
        return redirect(url_for("dashboard"))

    return render_template("new_ticket.html")

@app.route("/tickets/update/<int:ticket_id>", methods=["GET", "POST"])
def update_ticket(ticket_id):
    if "user_id" not in session or session["role"] != "admin":
        return redirect(url_for("login"))

    conn = sqlite3.connect("database.db")
    cursor = conn.cursor()

    if request.method == "POST":
        new_status = request.form["status"]
        cursor.execute("UPDATE tickets SET status=? WHERE id=?", (new_status, ticket_id))
        conn.commit()
        conn.close()
        flash("Ticket updated successfully!", "success")
        return redirect(url_for("dashboard"))

    cursor.execute("SELECT * FROM tickets WHERE id=?", (ticket_id,))
    ticket = cursor.fetchone()
    conn.close()
    return render_template("update_ticket.html", ticket=ticket)

@app.route("/logout")
def logout():
    session.clear()
    flash("You have been logged out.", "info")
    return redirect(url_for("login"))

if __name__ == "__main__":
    app.run(debug=True)
