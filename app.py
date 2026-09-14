from flask import Flask, render_template, request, redirect, session, flash
import sqlite3
from datetime import date
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)

app.secret_key = "jobtrack-secret-key"

def get_db_connection():
    conn = sqlite3.connect("jobtrack.db")
    conn.row_factory = sqlite3.Row
    return conn

@app.route("/signup", methods=["GET", "POST"])
def signup():

    if request.method == "POST":

        username = request.form["username"]
        email = request.form["email"]
        password = request.form["password"]

        hashed_password = generate_password_hash(password)

        conn = sqlite3.connect("jobtrack.db")

        try:

            conn.execute(
                """
                INSERT INTO users
                (username, email, password)
                VALUES (?, ?, ?)
                """,
                (username, email, hashed_password)
            )

            conn.commit()

        except sqlite3.IntegrityError:

            conn.close()

            flash("Username or email already exists.", "error")
            return redirect("/signup")

        conn.close()

        flash("Account created successfully! Please login.", "success")

        return redirect("/login")

    return render_template("signup.html")

@app.route("/login", methods=["GET", "POST"])
def login():

    if request.method == "POST":

        email = request.form["email"]
        password = request.form["password"]

        conn = sqlite3.connect("jobtrack.db")
        conn.row_factory = sqlite3.Row

        user = conn.execute(
            "SELECT * FROM users WHERE email = ?",
            (email,)
        ).fetchone()

        conn.close()

        if user and check_password_hash(user["password"], password):

            session["user_id"] = user["id"]
            session["username"] = user["username"]

            return redirect("/")

        flash("Invalid email or password.", "error")
        return redirect("/login")

    return render_template("login.html")

@app.route("/logout")
def logout():

    session.clear()

    return redirect("/login")

@app.route("/edit/<int:id>", methods=["GET", "POST"])
def edit_application(id):
    if "user_id" not in session:
        return redirect("/login")

    conn = sqlite3.connect("jobtrack.db")
    conn.row_factory = sqlite3.Row

    if request.method == "POST":

        old_application = conn.execute(
            """
            SELECT status
            FROM applications
            WHERE id = ?
            AND user_id = ?
            """,
            (id, session["user_id"])
        ).fetchone()

        if old_application is None:
            conn.close()
            return "Application not found.", 404

        old_status = old_application["status"]

        company = request.form["company"]
        role = request.form["role"]
        status = request.form["status"]
        date = request.form["date"]
        notes = request.form["notes"]
        interview_date = request.form.get("interview_date", "")
        interview_time = request.form.get("interview_time", "")
        interview_type = request.form.get("interview_type", "")
        follow_up_date = request.form.get("follow_up_date", "")
        company_url = request.form.get("company_url", "")
        job_url = request.form.get("job_url", "")

        conn.execute(
            """
            UPDATE applications
            SET company = ?,
                role = ?,
                status = ?,
                date = ?,
                notes = ?,
                interview_date = ?,
                interview_time = ?,
                interview_type = ?,
                follow_up_date = ?,
                company_url = ?,
                job_url = ?
            WHERE id = ?
            AND user_id = ?
            """,
            (
                company,
                role,
                status,
                date,
                notes,
                interview_date,
                interview_time,
                interview_type,
                follow_up_date,
                company_url,
                job_url,
                id,
                session["user_id"]
            )
        )

        # Record status change

        if old_status != status:

            conn.execute(
                """
                INSERT INTO status_history
                (application_id, status, changed_at)
                VALUES (?, ?, datetime('now'))
                """,
                (id, status)
            )

        conn.commit()
        conn.close()

        return redirect("/")


    application = conn.execute(
    """
    SELECT *
    FROM applications
    WHERE id = ?
    AND user_id = ?
    """,
    (id, session["user_id"])
    ).fetchone()

    if application is None:
        conn.close()
        return "Application not found.", 404

    conn.close()

    return render_template(
        "edit.html",
        application=application
    )

@app.route("/details/<int:id>")
def application_details(id):
    if "user_id" not in session:
        return redirect("/login")

    conn = sqlite3.connect("jobtrack.db")
    conn.row_factory = sqlite3.Row

    application = conn.execute(
    """
    SELECT *
    FROM applications
    WHERE id = ?
    AND user_id = ?
    """,
    (id, session["user_id"])
    ).fetchone()

    if application is None:
        conn.close()
        return "Application not found.", 404

    status_history = conn.execute(
    """
    SELECT *
    FROM status_history
    WHERE application_id = ?
    ORDER BY changed_at DESC
    """,
    (id,)
    ).fetchall()

    conn.close()

    return render_template(
        "details.html",
        application=application,
        status_history=status_history
    )



@app.route("/notes/<int:id>", methods=["GET", "POST"])
def view_notes(id):
    if "user_id" not in session:
        return redirect("/login")

    conn = sqlite3.connect("jobtrack.db")
    conn.row_factory = sqlite3.Row

    if request.method == "POST":

        notes = request.form["notes"]

        conn.execute(
            """
            UPDATE applications
            SET notes = ?
            WHERE id = ?
            AND user_id = ?
            """,
            (notes, id, session["user_id"])
        )

        conn.commit()

    application = conn.execute(
        """
        SELECT *
        FROM applications
        WHERE id = ?
        AND user_id = ?
        """,
        (id, session["user_id"])
    ).fetchone()

    if application is None:
        conn.close()
        return "Application not found.", 404

    conn.close()

    return render_template(
        "notes.html",
        application=application
    )

@app.route("/add", methods=["POST"])
def add_application():
    if "user_id" not in session:
        return redirect("/login")

    company = request.form["company"]
    role = request.form["role"]
    status = request.form["status"]
    date = request.form["date"]
    notes = request.form["notes"]
    interview_date = request.form.get("interview_date", "")
    interview_time = request.form.get("interview_time", "")
    interview_type = request.form.get("interview_type", "")
    follow_up_date = request.form.get("follow_up_date", "")
    company_url = request.form.get("company_url", "")
    job_url = request.form.get("job_url", "")

    user_id = session["user_id"]

    conn = sqlite3.connect("jobtrack.db")

    cursor = conn.execute(
    """
    INSERT INTO applications
    (
        company,
        role,
        status,
        date,
        notes,
        interview_date,
        interview_time,
        interview_type,
        follow_up_date,
        company_url,
        job_url,
        user_id
    )
    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """,
    (
        company,
        role,
        status,
        date,
        notes,
        interview_date,
        interview_time,
        interview_type,
        follow_up_date,
        company_url,
        job_url,
        user_id
    )
)

    # Record initial status

    application_id = cursor.lastrowid

    conn.execute(
        """
        INSERT INTO status_history
        (application_id, status, changed_at)
        VALUES (?, ?, datetime('now'))
        """,
        (application_id, status)
    )

    conn.commit()
    conn.close()

    return redirect("/")

@app.route("/delete/<int:id>")
def delete_application(id):
    if "user_id" not in session:
        return redirect("/login")

    conn = sqlite3.connect("jobtrack.db")

    conn.execute(
        """
        DELETE FROM applications
        WHERE id = ?
        AND user_id = ?
        """,
        (id, session["user_id"])
    )

    conn.commit()
    conn.close()

    return redirect("/")

@app.route("/")
def home():

    if "user_id" not in session:
        return redirect("/login")

    user_id = session["user_id"]

    search = request.args.get("search", "")
    status = request.args.get("status", "")
    sort = request.args.get("sort", "newest")

    conn = sqlite3.connect("jobtrack.db")
    conn.row_factory = sqlite3.Row

    query = "SELECT * FROM applications WHERE user_id = ?"
    params = [user_id]

    # Search by company or role
    if search:
        query += " AND (company LIKE ? OR role LIKE ?)"
        params.append("%" + search + "%")
        params.append("%" + search + "%")

    # Filter by status
    if status:
        query += " AND status = ?"
        params.append(status)

    # Sorting
    if sort == "oldest":
        query += " ORDER BY date ASC"

    elif sort == "company_asc":
        query += " ORDER BY company ASC"

    elif sort == "company_desc":
        query += " ORDER BY company DESC"

    else:
        query += " ORDER BY date DESC"

    applications = conn.execute(
        query,
        params
    ).fetchall()

    # Next Follow-ups

    today = date.today().isoformat()

    follow_ups = conn.execute(
    """
    SELECT *
    FROM applications
    WHERE user_id = ?
    AND follow_up_date IS NOT NULL
    AND follow_up_date != ''
    ORDER BY follow_up_date ASC
    """,
    (user_id,)
    ).fetchall()

    overdue_followups = []
    today_followups = []
    upcoming_followups = []

    for application in follow_ups:

        if application["follow_up_date"] < today:
            overdue_followups.append(application)

        elif application["follow_up_date"] == today:
            today_followups.append(application)

        else:
            upcoming_followups.append(application)

    # Dashboard counts

    total = conn.execute(
    "SELECT COUNT(*) FROM applications WHERE user_id = ?",
    (user_id,)
    ).fetchone()[0]

    applied = conn.execute(
    "SELECT COUNT(*) FROM applications WHERE user_id = ? AND status = 'Applied'",
    (user_id,)
    ).fetchone()[0]

    interviews = conn.execute(
    "SELECT COUNT(*) FROM applications WHERE user_id = ? AND status = 'Interview'",
    (user_id,)
    ).fetchone()[0]

    rejected = conn.execute(
    "SELECT COUNT(*) FROM applications WHERE user_id = ? AND status = 'Rejected'",
    (user_id,)
    ).fetchone()[0]

    offers = conn.execute(
    "SELECT COUNT(*) FROM applications WHERE user_id = ? AND status = 'Offer'",
    (user_id,)
    ).fetchone()[0]

    conn.close()

    return render_template(
        "index.html",
        applications=applications,
        total=total,
        applied=applied,
        interviews=interviews,
        rejected=rejected,
        offers=offers,
        search=search,
        status=status,
        sort=sort,
        overdue_followups=overdue_followups,
        today_followups=today_followups,
        upcoming_followups=upcoming_followups
    )

if __name__ == "__main__":
    app.run(debug=True)