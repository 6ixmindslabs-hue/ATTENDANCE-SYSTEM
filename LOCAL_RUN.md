# Local Run Guide

## 1. Prepare Supabase

1. Open your Supabase project.
2. Go to SQL Editor.
3. Run `supabase_schema.sql` from this project root.

You can also use Alembic from PowerShell after backend dependencies are ready:

```powershell
.\backend\venv\Scripts\alembic.exe upgrade head
```

The backend connects directly to Supabase Postgres. Do not put the Supabase database URL in frontend files.

## 2. Check Backend Env

`backend/.env` should contain:

```env
SUPABASE_DATABASE_URL=postgresql://postgres:YOUR_PASSWORD@db.YOUR_PROJECT_REF.supabase.co:5432/postgres
DATABASE_SSLMODE=require
FRONTEND_ORIGINS=http://localhost:5173,http://127.0.0.1:5173,https://mpnmjecattendance.duckdns.org
```

The password in a URL must be percent-encoded if it contains special characters such as `@`, `#`, `%`, `/`, `?`, or `^`.

## 3. Install Required Local Tools

- Python 3.11, or `uv` with internet access so the launcher can create a Python 3.11 venv
- Node.js 20 or newer

The backend launcher first tries the bundled `backend/venv` folder. If that is not usable, it creates `backend/.venv` automatically. If normal Python is not installed but `uv` is available, it uses `uv` to create the venv.

## 4. Start Locally

From the project root:

```powershell
.\start-backend.ps1
```

In another PowerShell window:

```powershell
.\start-frontend.ps1
```

Open:

```text
http://127.0.0.1:5173
```

## 5. Create Admin Account

After the backend can connect to Supabase:

```powershell
.\backend\.venv\Scripts\python.exe -m backend.seed_admin
```

This uses `ADMIN_EMAIL` and `ADMIN_PASSWORD` from `backend/.env`.

## 6. Student Login

Students now need:

- Register number
- Date of birth

Make sure each student record has `dob` filled during enrollment or edit.

## 7. Backend Tests

Run:

```powershell
.\backend\venv\Scripts\pytest.exe
```
