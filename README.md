<div align="center">

# 🏛️ LIMS — Library Information Management System

<img src="https://img.shields.io/badge/Django-Web_Framework-092E20?style=for-the-badge&logo=django&logoColor=white"/>
<img src="https://img.shields.io/badge/Python-3.x-3776AB?style=for-the-badge&logo=python&logoColor=white"/>
<img src="https://img.shields.io/badge/SQLite-Database-003B57?style=for-the-badge&logo=sqlite&logoColor=white"/>
<img src="https://img.shields.io/badge/HTML5-Templates-E34F26?style=for-the-badge&logo=html5&logoColor=white"/>
<img src="https://img.shields.io/badge/Status-Active-brightgreen?style=for-the-badge"/>

<br/>

> A full-stack **Library Information Management System** built with **Django** — manage books, members, and library operations through a clean web interface.

</div>

---

## ✨ Features

- 📚 **Book Management** — Add, update, search, and remove books from the catalog
- 👤 **Member Management** — Register and manage library members
- 🔄 **Issue & Return** — Track book issuances and returns with due dates
- 🔍 **Search & Filter** — Quickly find books or members by name, ID, or category
- 🛡️ **Admin Panel** — Powered by Django's built-in admin interface
- 🗄️ **SQLite Database** — Lightweight, file-based database with no extra setup

---

## 📁 Project Structure

```
django-project/
│
├── lim_app/                # Core Django application
│   ├── migrations/         # Database migration files
│   ├── templates/          # HTML templates for views
│   ├── static/             # App-level static files
│   ├── models.py           # Database models (Book, Member, Issue, etc.)
│   ├── views.py            # View logic & request handling
│   ├── urls.py             # App-level URL routing
│   ├── forms.py            # Django forms
│   └── admin.py            # Admin panel configuration
│
├── lims_project/           # Django project configuration
│   ├── settings.py         # Project settings
│   ├── urls.py             # Root URL configuration
│   └── wsgi.py             # WSGI entry point
│
├── static/
│   └── images/             # Static image assets
│
├── db.sqlite3              # SQLite database
└── manage.py               # Django management CLI
```

---

## 🚀 Getting Started

```bash
# 1. Clone the repository
git clone https://github.com/Manav-020/django-project.git
cd django-project

# 2. Create and activate a virtual environment
python -m venv venv
source venv/bin/activate        # macOS/Linux
venv\Scripts\activate           # Windows

# 3. Install Django
pip install django

# 4. Apply database migrations
python manage.py migrate

# 5. Create a superuser (for admin access)
python manage.py createsuperuser

# 6. Run the development server
python manage.py runserver
```

Then open [http://127.0.0.1:8000](http://127.0.0.1:8000) in your browser.
Admin panel is available at [http://127.0.0.1:8000/admin](http://127.0.0.1:8000/admin).

---

## 🛠️ Tech Stack

| Layer | Technology |
|-------|------------|
| **Backend** | Django (Python) |
| **Frontend** | HTML5, CSS3 (Django Templates) |
| **Database** | SQLite3 |
| **Admin** | Django Admin Interface |
| **ORM** | Django ORM |

---

## 🗃️ Database Models

| Model | Description |
|-------|-------------|
| `Book` | Stores book details — title, author, category, availability |
| `Member` | Library member records — name, contact, membership info |
| `Issue` | Tracks which member borrowed which book and when |

---

## 👤 Author

**Manav**
- GitHub: [@Manav-020](https://github.com/Manav-020)

---

## 📄 License

This project is for **educational purposes**. Feel free to explore and learn from it.

---

<div align="center">
  <p>Built with ☕ and Django — where every <code>migrate</code> felt like a small victory</p>
</div>
