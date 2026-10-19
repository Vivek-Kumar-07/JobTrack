# JobTrack — Job & Internship Application Tracker

JobTrack is a Flask-based web application that helps job seekers organize their job and internship applications, manage interview details and follow-ups, and monitor their application progress through a dashboard.

**[Live Demo](https://jobtrack-lbsy.onrender.com/login) · [GitHub Repository](https://github.com/Vivek-Kumar-07/JobTrack)**

## Features

- **User Authentication:** Account registration, login, password hashing, and session-based authentication.
- **Application Management:** Add, edit, view, and delete job and internship applications.
- **Search & Filtering:** Search by company or role, filter by application status and date range, and sort applications.
- **Interview & Follow-up Tracking:** Store interview details, notes, company links, job links, and follow-up dates.
- **Application Dashboard:** Track total applications, applied positions, interviews, rejections, and offers.
- **Monthly Analytics:** Review application activity and monthly interview, rejection, and offer statistics.
- **Status History:** Keep a record of application status changes.
- **CSV Export:** Export your applications for personal record-keeping.
- **User Data Isolation:** Application queries are scoped to the authenticated user.

## Tech Stack

- **Backend:** Python, Flask
- **Database:** SQLite for local development; PostgreSQL when `DATABASE_URL` is configured
- **Frontend:** HTML, CSS, JavaScript
- **Charts:** Chart.js
- **Security:** Werkzeug password hashing, Flask-WTF CSRF protection, session-based authentication
- **Deployment:** Render
- **Production Server:** Gunicorn

## Run Locally

### 1. Clone the repository

```bash
git clone https://github.com/Vivek-Kumar-07/JobTrack.git
cd JobTrack
```

### 2. Create and activate a virtual environment

On Windows PowerShell:

```powershell
python -m venv venv
.\venv\Scripts\Activate.ps1
```

### 3. Install dependencies

```powershell
python -m pip install -r requirements.txt
```

### 4. Configure the environment

For a local SQLite setup, ensure `DATABASE_URL` is not set in the current PowerShell session:

```powershell
Remove-Item Env:DATABASE_URL -ErrorAction SilentlyContinue
$env:SECRET_KEY = (python -c "import secrets; print(secrets.token_hex(32))")
```

These commands configure a temporary development secret for the current terminal session. Use a securely managed, persistent secret for deployment.

### 5. Initialize the SQLite database

```powershell
python database.py
```

### 6. Start the application

```powershell
python app.py
```

Open [http://127.0.0.1:5000](http://127.0.0.1:5000) in your browser.

## Database and Deployment Notes

JobTrack supports two database configurations:

- **SQLite:** Used when `DATABASE_URL` is not configured.
- **PostgreSQL:** Used when `DATABASE_URL` points to a PostgreSQL database.

For a new PostgreSQL database, `init_postgres.py` provides schema initialization. Configure `DATABASE_URL` and `SECRET_KEY` securely in your deployment environment. The application can be served using Gunicorn with `gunicorn app:app`.

Do not commit database credentials, production secrets, or private user data to GitHub.

## What I Learned

- Building a full-stack web application using Flask and SQLite/PostgreSQL.
- Implementing authentication and user-specific data access.
- Designing database tables, relationships, indexes, and queries.
- Validating form input and protecting state-changing requests with CSRF protection.
- Building dashboards and analytics from application data.
- Deploying a Flask application and configuring its production database.

## Screenshots

### Dashboard & Analytics
![JobTrack Dashboard](screenshots/Dashboard%20%26%20Analytics.png)

### Follow-ups & Applications
![Follow-ups and Applications](screenshots/Follow-ups%20%26%20Applications.png)

### Add Application Form
![Add Application Form](screenshots/Add%20Application%20Form.png)

### Application Details
![Application Details](screenshots/Application%20Details.png)

### Application Details & Status History
![Application Details and Status History](screenshots/Application%20Details%20%26%20Status%20History.png)

## Author

**Vivek Kumar**  
B.Tech in Data Science, Haldia Institute of Technology

- [GitHub](https://github.com/Vivek-Kumar-07)
- [JobTrack Live Demo](https://jobtrack-lbsy.onrender.com/login)
