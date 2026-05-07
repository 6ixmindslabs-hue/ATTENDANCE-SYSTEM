# Smart Attendance System

This frontend is wired to the FastAPI backend and a Supabase/PostgreSQL database used by the attendance system.

## Stack

- Frontend: React + Vite
- Backend: FastAPI
- Database: Supabase Postgres
- Face recognition: InsightFace via the backend

## Project Structure

- `frontend/`: React application
- `backend/`: FastAPI API, SQLAlchemy models, Supabase/PostgreSQL connection, face recognition logic

## Backend Setup

1. Create a Supabase project.

2. In Supabase, open your project, choose **Connect**, and copy a database connection string.

For this long-running FastAPI backend, use the Supavisor **Session pooler** connection string if your network does not support IPv6. A direct connection also works if your environment supports it.

3. Copy the backend env template and update it with your Supabase credentials:

```powershell
Copy-Item backend/.env.example backend/.env
```

Set `SUPABASE_DATABASE_URL` in `backend/.env`:

```env
SUPABASE_DATABASE_URL=postgresql://postgres.your_project_ref:your_password@aws-0-your-region.pooler.supabase.com:5432/postgres
DATABASE_SSLMODE=require
```

Supabase sometimes shows URLs starting with `postgres://`; this project accepts those and normalizes them for SQLAlchemy.

4. Install backend dependencies in the existing virtual environment or recreate one if needed.

5. Start the API from the project root:

```powershell
cd C:\Users\dhine\Desktop\ATTENDANCE_SYSTEM
.\backend\venv\Scripts\uvicorn.exe backend.main:app --reload
```

The backend now supports root-level startup with `backend.main:app`, so it does not depend on launching from inside the `backend` folder.
The backend creates the required tables on startup.

## Admin Seeding

You can create the first admin account after the database is configured:

```powershell
cd C:\Users\dhine\Desktop\ATTENDANCE_SYSTEM
.\backend\venv\Scripts\python.exe -m backend.seed_admin
```

If `ADMIN_EMAIL` and `ADMIN_PASSWORD` are present in `backend/.env`, the script will use them automatically.

## Frontend Setup

1. Copy the frontend env template:

```powershell
Copy-Item frontend/.env.example frontend/.env
```

2. If your backend is not running on `http://127.0.0.1:8000`, update `VITE_API_URL` in `frontend/.env`.

3. Start the frontend:

```powershell
cd C:\Users\dhine\Desktop\ATTENDANCE_SYSTEM\frontend
npm install
npm run dev
```

## API Wiring

The frontend uses `frontend/src/api.js` for all backend communication:

- Authentication: `/token`, `/me`
- Dashboard: `/dashboard/overview`, `/dashboard/summary`, `/students/me`
- Users: `/users/`, `/users/face-embedding`, `/users/{id}/attendance`
- Attendance: `/attendance/`, `/attendance/records`, `/attendance/recent`, `/attendance/manual`, `/recognize/`
- Settings: `/settings`

If `VITE_API_URL` is not set, the frontend now automatically targets `http://<current-host>:8000`, which makes local LAN and same-machine development work more reliably than a hardcoded `127.0.0.1`.

## Build Check

Run the frontend production build:

```powershell
cd C:\Users\dhine\Desktop\ATTENDANCE_SYSTEM\frontend
npm run build
```

## Notes

- Supabase/PostgreSQL is configured through `backend/.env` using `SUPABASE_DATABASE_URL`.
- `DATABASE_URL` is still supported as a fallback for local PostgreSQL.
- If neither `SUPABASE_DATABASE_URL` nor `DATABASE_URL` is set, the backend uses a local SQLite database path. The intended setup for this project is Supabase Postgres.
- CORS origins can be adjusted with `FRONTEND_ORIGINS` in `backend/.env`.
