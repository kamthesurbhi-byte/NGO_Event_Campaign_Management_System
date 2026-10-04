from flask import Flask, render_template, request
import mysql.connector

app = Flask(__name__)


# =========================
# Database Connection
# =========================

db = mysql.connector.connect(
    host="localhost",
    user="root",
    password="",
    database="ngo_management"
)


# =========================
# Home Page
# =========================

@app.route("/")
def home():
    return render_template("index.html")


# =========================
# About Page
# =========================

@app.route("/about")
def about():
    return render_template("about.html")


# =========================
# Projects / Activities Page
# =========================

@app.route("/projects")
def projects():

    cursor = db.cursor(dictionary=True)

    cursor.execute("SELECT * FROM projects")

    projects_data = cursor.fetchall()

    cursor.close()

    return render_template(
        "projects.html",
        projects=projects_data
    )


# =========================
# Volunteer Registration
# =========================

@app.route("/volunteer", methods=["GET", "POST"])
def volunteer():
    if request.method == "POST":
        name = request.form["name"]
        email = request.form["email"]
        phone = request.form["phone"]
        address = request.form["address"]
        skills = request.form["skills"]

        cursor = db.cursor()

        sql = """
        INSERT INTO volunteers
        (name, email, phone, address, skills)
        VALUES (%s, %s, %s, %s, %s)
        """

        values = (name, email, phone, address, skills)

        cursor.execute(sql, values)
        db.commit()
        cursor.close()

        return render_template("volunteer_success.html")

    return render_template("volunteer.html")

# =========================
# Registered Volunteers
# =========================

@app.route("/volunteers")
def volunteers():

    cursor = db.cursor(dictionary=True)

    cursor.execute(
        "SELECT * FROM volunteers ORDER BY id DESC"
    )

    volunteers_data = cursor.fetchall()

    cursor.close()

    return render_template(
        "volunteers.html",
        volunteers=volunteers_data
    )
# =========================
# Add Event
# =========================

@app.route("/add-event", methods=["GET", "POST"])
def add_event():

    if request.method == "POST":

        event_name = request.form["event_name"]
        description = request.form["description"]
        event_date = request.form["event_date"]
        location = request.form["location"]
        status = request.form["status"]

        cursor = db.cursor()

        sql = """
        INSERT INTO events
        (event_name, description, event_date, location, status)
        VALUES (%s, %s, %s, %s, %s)
        """

        values = (
            event_name,
            description,
            event_date,
            location,
            status
        )

        cursor.execute(sql, values)

        db.commit()

        cursor.close()

        return render_template("event_success.html")

    return render_template("add_event.html")
# =========================
# View Events
# =========================

@app.route("/events")
def events():

    cursor = db.cursor(dictionary=True)

    cursor.execute(
        "SELECT * FROM events ORDER BY event_date DESC"
    )

    events_data = cursor.fetchall()

    cursor.close()

    return render_template(
        "events.html",
        events=events_data
    )
# =========================
# Contact Page
# =========================

@app.route("/contact")
def contact():
    return render_template("contact.html")
@app.route("/dashboard")
def dashboard():
    cursor = db.cursor()

    cursor.execute("SELECT COUNT(*) FROM volunteers")
    total_volunteers = cursor.fetchone()[0]

    cursor.execute("SELECT COUNT(*) FROM events")
    total_events = cursor.fetchone()[0]

    cursor.execute("SELECT COUNT(*) FROM projects")
    total_projects = cursor.fetchone()[0]

    cursor.close()

    return render_template(
        "dashboard.html",
        total_volunteers=total_volunteers,
        total_events=total_events,
        total_projects=total_projects
    )

# =========================
# Run Application
# =========================

if __name__ == "__main__":
    app.run(debug=True)