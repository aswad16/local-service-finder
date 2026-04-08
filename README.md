# LocalServe — Django Local Service Finder

A full-featured local service marketplace built with **Django 4.2**, **MySQL**, **JWT auth**, and **Claude AI** recommendations. Premium dark UI.

---

## 🚀 Quick Start

### 1. Create MySQL Database
```sql
CREATE DATABASE localservice_db CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
```

### 2. Clone & Setup Environment
```bash
cd localservice
cp .env.example .env
# Edit .env with your DB credentials and Anthropic API key
```

### 3. Create Virtual Environment & Install
```bash
python -m venv venv
source venv/bin/activate        # Windows: venv\Scripts\activate
pip install -r requirements.txt
```

### 4. Run Migrations
```bash
python manage.py makemigrations
python manage.py migrate
```

### 5. Seed Demo Data
```bash
python seed.py
```

### 6. Create Admin User (or use seeded admin)
```bash
python create_admin.py
# OR use seeded: admin / Admin@123
```

### 7. Run Development Server
```bash
python manage.py runserver
```

Visit: **http://localhost:8000**

---

## 🔑 Default Credentials (after seed)

| Role     | Username        | Password       | URL                  |
|----------|-----------------|----------------|----------------------|
| Admin    | admin           | Admin@123      | /adminpanel/         |
| Provider | rajesh_electric | Provider@123   | /dashboard/          |
| Customer | arun_kumar      | Customer@123   | /                    |

---

## 📁 Project Structure

```
localservice/
├── localservice/          # Django project settings
│   ├── settings.py
│   └── urls.py
├── users/                 # Custom user model + JWT auth
├── services/              # Service listings + provider dashboard
├── reviews/               # Review system
├── search/                # Search + Claude AI recommendations
├── adminpanel/            # Custom admin panel
├── templates/             # All HTML templates
│   ├── base.html
│   ├── home.html
│   ├── users/
│   ├── services/
│   ├── search/
│   └── adminpanel/
├── static/
│   ├── css/main.css       # Premium dark UI
│   ├── css/admin.css      # Admin panel styles
│   ├── js/main.js         # Frontend JS
│   ├── js/auth.js         # JWT + role selector
│   └── js/admin.js        # Admin panel JS
├── media/                 # Uploaded files
├── manage.py
├── seed.py                # Demo data seeder
├── create_admin.py        # Admin creation utility
├── requirements.txt
└── .env.example
```

---

## ⚙️ Key Features

- **Multi-role auth**: Customer, Provider, Admin with role-based redirects
- **JWT tokens**: Access + refresh tokens stored in sessionStorage
- **Claude AI**: Smart search tips + service recommendations via `/search/recommend/`
- **Provider dashboard**: KPIs, service management, review tracking
- **Custom admin panel**: `/adminpanel/` with stats, user/service/review/category management
- **REST API**: Full DRF API at `/api/` with JWT authentication
- **Premium dark UI**: Syne + DM Sans fonts, CSS variables, smooth animations

---

## 🌐 Key URLs

| Page | URL |
|------|-----|
| Home | `/` |
| Search | `/search/?q=electrician` |
| AI Recommendations | `/search/recommend/` |
| Browse Services | `/services/` |
| Provider Dashboard | `/dashboard/` |
| Admin Panel | `/adminpanel/` |
| Django Admin | `/admin/` |
| API | `/api/` |

---

## 🔧 Environment Variables (`.env`)

```
SECRET_KEY=your-secret-key
DEBUG=True
DB_NAME=localservice_db
DB_USER=root
DB_PASSWORD=yourpassword
DB_HOST=localhost
DB_PORT=3306
your-api-key-here```

---

## 📦 Tech Stack

- **Backend**: Django 4.2, Django REST Framework
- **Database**: MySQL (via mysqlclient)
- **Auth**: Django sessions + JWT (djangorestframework-simplejwt)
- **AI**: Anthropic Claude API (`claude-opus-4-5`)
- **Static files**: WhiteNoise
- **Frontend**: Vanilla JS, CSS custom properties, Google Fonts
