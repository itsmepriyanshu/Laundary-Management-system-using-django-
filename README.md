# 🧺 Laundry Management System using Django

This is a web-based Laundry Management System built using **Django**. It allows users to manage orders, track laundry status, and maintain records easily.

## Features

- User authentication (login/register)
- Admin dashboard
- Manage customers and laundry items
- Track order status (e.g., pending, washing, delivered)
- Invoice generation
- Responsive interface (if front-end styling is applied)

## Tech Stack

- Backend: Django (Python)
- Frontend: HTML, CSS, Bootstrap
- Database: SQLite
- Version Control: Git & GitHub

## Installation Guide

1. **Clone the repository**  
   ```bash
   git clone https://github.com/itsmepriyanshu/Laundary-Management-system-using-django-.git
   cd Laundary-Management-system-using-django-
2. Create a virtual environment

python -m venv venv
venv\Scripts\activate    # On Windows
# OR
source venv/bin/activate # On macOS/Linux

3. Install dependencies
   
pip install -r requirements.txt
If requirements.txt is missing, generate one with:
pip freeze > requirements.txt

4. Apply migrations

python manage.py makemigrations
python manage.py migrate

5.Create a superuser

python manage.py createsuperuser

Follow the prompts to set username, email, and password.

6.Run the server
python manage.py runserver
Then open http://127.0.0.1:8000/ in your browser.


Project Structure (Typical Django)

laundry/
├── manage.py
├── db.sqlite3
├── requirements.txt
├── your_app_name/
│   ├── migrations/
│   ├── static/
│   ├── templates/
│   ├── admin.py
│   ├── models.py
│   ├── views.py
│   └── urls.py
├── laundry_project/  # Your main project folder
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
