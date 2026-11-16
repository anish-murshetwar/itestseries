# iTestSeries

A Django-based study resource platform for browsing and accessing
chapter-wise learning materials.

## Project overview

iTestSeries currently focuses on **ICSE Class 9 and Class 10** study
resources. The site organizes materials by board, class, subject, and
chapter so students can find relevant resources more easily.

## Current features

-   Browse boards, classes, subjects, and chapters.
-   View study materials associated with chapters.
-   Search notes, papers, and other study resources.
-   Display featured study materials on the homepage.
-   Mark materials as free or paid and control publication status.
-   Manage boards, classes, subjects, chapters, and study materials
    through Django Admin.
-   Upload PDF study materials through the admin interface, with file
    type and size validation.
-   Register, log in, and log out using user accounts.
-   Require users to log in before downloading study materials.
-   Reset forgotten passwords through the password-reset workflow.
-   Manage registered users through Django Admin, including searching,
    filtering, activating, and deactivating accounts.

## Technology stack

-   **Backend:** Python, Django 5.2
-   **Database:** PostgreSQL
-   **Frontend:** HTML, CSS, Bootstrap 5
-   **Static files:** WhiteNoise
-   **Email:** Django email backend; SMTP configuration is prepared for
    future Brevo integration.
-   **Deployment:** Render (application hosting and PostgreSQL)

## Getting started

These instructions describe a typical local setup. Use the
environment-variable names expected by the project's Django settings.

### 1. Clone the repository

``` bash
git clone https://github.com/anish-murshetwar/itestseries.git
cd itestpapers
```

### 2. Create and activate a virtual environment

On Ubuntu / WSL:

``` bash
python3 -m venv .venv
source .venv/bin/activate
```

### 3. Install dependencies

``` bash
pip install -r requirements.txt
```

### 4. Configure environment variables

Create a `.env` file in the project root. Add the values required by
your local Django settings, including:

-   `SECRET_KEY`
-   `DEBUG`
-   `DATABASE_URL`
-   `ALLOWED_HOSTS`
-   `CSRF_TRUSTED_ORIGINS` (if required by the current settings)

Email settings can also be configured through environment variables:

-   `EMAIL_BACKEND`
-   `EMAIL_HOST`
-   `EMAIL_PORT`
-   `EMAIL_HOST_USER`
-   `EMAIL_HOST_PASSWORD`
-   `DEFAULT_FROM_EMAIL`

Local development can use Django's console email backend. In that mode,
password-reset emails are printed in the development terminal rather
than delivered to an inbox. Real email delivery requires valid SMTP
credentials and a verified sender address.

Do not commit `.env` or place real credentials in this README.

### 5. Apply database migrations

Make sure PostgreSQL is running and the database connection is
configured, then run:

``` bash
python manage.py migrate
```

### 6. Create an admin account

``` bash
python manage.py createsuperuser
```

### 7. Start the development server

``` bash
python manage.py runserver
```

Open `http://127.0.0.1:8000/` in your browser. The Django admin is
available at `http://127.0.0.1:8000/admin/`.

## Project status

The core study-material catalog, homepage, search, Django admin
management, user registration, login, logout, authenticated PDF
downloads, and password-reset workflow have been implemented and tested
locally and on Render. Further refinements are planned separately.

## Security notes

-   Keep `.env`, secret keys, database credentials, and other private
    configuration out of version control.
-   Require authentication for study-material downloads.
-   Use valid SMTP credentials and a verified sender before enabling
    real password-reset email delivery.
-   Do not upload private student information or copyrighted study
    material unless you have permission to host it.
-   Review production settings before deploying changes.

## Repository

GitHub: https://github.com/anish-murshetwar/itestseries

The public-facing website brand is **iTestSeries**. The local project
folder and internal Django package names may still use `itestpapers`;
these do not need to be renamed for the public-facing brand change.
