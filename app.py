from flask import Flask, render_template, request, redirect, url_for
import sqlite3

app = Flask(__name__)
DATABASE = "events.db"

def get_db():
    return sqlite3.connect(DATABASE)

def init_db():
    conn = get_db()
    conn.execute("""
        CREATE TABLE IF NOT EXISTS events (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            date TEXT NOT NULL,
            venue TEXT NOT NULL,
            description TEXT NOT NULL
        )
    """)
    conn.execute("""
        CREATE TABLE IF NOT EXISTS registrations (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            event_id INTEGER NOT NULL,
            name TEXT NOT NULL,
            email TEXT NOT NULL
        )
    """)
    conn.commit()
    conn.close()

@app.route("/")
def home():
    conn = get_db()
    events = conn.execute("SELECT * FROM events ORDER BY date").fetchall()
    conn.close()
    return render_template("index.html", events=events)

@app.route("/add-event", methods=["GET", "POST"])
def add_event():
    if request.method == "POST":
        conn = get_db()
        conn.execute(
            "INSERT INTO events(title, date, venue, description) VALUES (?, ?, ?, ?)",
            (request.form["title"], request.form["date"],
             request.form["venue"], request.form["description"])
        )
        conn.commit()
        conn.close()
        return redirect(url_for("home"))
    return render_template("add_event.html")

@app.route("/register/<int:event_id>", methods=["GET", "POST"])
def register(event_id):
    conn = get_db()
    event = conn.execute("SELECT * FROM events WHERE id=?", (event_id,)).fetchone()
    if not event:
        conn.close()
        return "Event not found", 404

    if request.method == "POST":
        conn.execute(
            "INSERT INTO registrations(event_id, name, email) VALUES (?, ?, ?)",
            (event_id, request.form["name"], request.form["email"])
        )
        conn.commit()
        conn.close()
        return render_template("success.html",
                               name=request.form["name"], event=event)

    conn.close()
    return render_template("register.html", event=event)

@app.route("/registrations")
def registrations():
    conn = get_db()
    rows = conn.execute("""
        SELECT registrations.name, registrations.email,
               events.title, events.date
        FROM registrations
        JOIN events ON registrations.event_id = events.id
        ORDER BY events.date
    """).fetchall()
    conn.close()
    return render_template("registrations.html", registrations=rows)

@app.route("/health")
def health():
    return {"status": "ok"}

init_db()

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=False)
