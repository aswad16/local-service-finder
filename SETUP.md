# LocalServe — Windows Setup Guide

## STEP 1 — Create the MySQL database (DO THIS FIRST)

Open **MySQL Command Line Client** or **MySQL Workbench** and run:

```sql
CREATE DATABASE localservice_db CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
```

To verify it was created:
```sql
SHOW DATABASES;
```

You should see `localservice_db` in the list.

---

## STEP 2 — Edit your .env file

Open `.env` in Notepad (it's inside the `localservice/` folder):

```
DB_NAME=localservice_db
DB_USER=root
DB_PASSWORD=YOUR_MYSQL_ROOT_PASSWORD_HERE
DB_HOST=localhost
DB_PORT=3306
```

Change `YOUR_MYSQL_ROOT_PASSWORD_HERE` to your actual MySQL password.

---

## STEP 3 — Install dependencies

```powershell
pip install -r requirements.txt
```

If `mysqlclient` fails, install PyMySQL instead:
```powershell
pip install pymysql
```

---

## STEP 4 — Run migrations

```powershell
python manage.py makemigrations
python manage.py migrate
```

---

## STEP 5 — Seed demo data

```powershell
python seed.py
```

---

## STEP 6 — Start the server

```powershell
python manage.py runserver
```

Visit: http://127.0.0.1:8000

---

## Login Credentials (after seeding)

| Role     | Username        | Password     | URL                              |
|----------|-----------------|--------------|----------------------------------|
| Admin    | admin           | Admin@123    | http://127.0.0.1:8000/adminpanel |
| Provider | rajesh_electric | Provider@123 | http://127.0.0.1:8000/dashboard  |
| Customer | arun_kumar      | Customer@123 | http://127.0.0.1:8000            |

---

## Troubleshooting

### `Unknown database 'localservice_db'`
You haven't created the MySQL database yet. Go back to **Step 1**.

### `Access denied for user 'root'`
Your MySQL password in `.env` is wrong. Double-check `DB_PASSWORD`.

### `mysqlclient` build error
Install PyMySQL: `pip install pymysql` — the project auto-detects it.

### `No module named 'decouple'`
This version doesn't use decouple. Make sure you downloaded the latest ZIP.

### URL namespace warning (non-fatal)
Fixed in the latest ZIP — just a warning, not a crash.
