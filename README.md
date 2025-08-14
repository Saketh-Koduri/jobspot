# JobSpot

live view demo : https://jobspot-ecor.onrender.com/users/login/

Django-based job board where **Employers** post jobs & manage applicants, and **Job Seekers** browse & apply.

## Features
- Role-based access (Job Seeker / Employer / Admin)
- Search & filter jobs
- Post, apply, and track applications
- Responsive UI with Bootstrap

## Tech Stack
Django • Python • PostgreSQL (Render) • SQLite (local) • Bootstrap

---

## Local Setup

# 1. Clone & enter project
git clone https://github.com/Saketh-Koduri/jobspot.git
cd jobspot

# 2. Create venv & activate
python -m venv venv
venv\Scripts\activate   # Windows
# source venv/bin/activate  # Mac/Linux

# 3. Install deps
pip install -r requirements.txt

# 4. Migrate & create superuser
python manage.py migrate
python manage.py createsuperuser


If you put this in your repo, it’ll stay **one scroll long** and still cover everything from GitHub → Render deployment.  

Do you also want me to make this README **include your actual Render live link** so recruiters can click it instantly?


# 5. Run
python manage.py runserver
