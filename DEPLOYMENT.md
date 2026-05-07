# Deployment

This project is set up for:

- Backend API on Render
- Frontend app on Vercel
- Database on Supabase Postgres

## Render Backend

Use the included `render.yaml` Blueprint, or create a Render Web Service manually with:

- Runtime: Python
- Build command: `pip install --upgrade pip setuptools wheel && pip install -r backend/requirements.txt`
- Start command: `uvicorn backend.main:app --host 0.0.0.0 --port $PORT`
- Health check path: `/`

Set these Render environment variables:

```env
SUPABASE_DATABASE_URL=your_supabase_postgres_connection_string
DATABASE_SSLMODE=require
DATABASE_CONNECT_TIMEOUT=5
SECRET_KEY=your_long_random_secret
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
FACE_RECOGNITION_THRESHOLD=0.40
FACE_RECOGNITION_MIN_MARGIN=0.03
INSIGHTFACE_MODEL_NAME=buffalo_l
INSIGHTFACE_DET_SIZE=320
PRELOAD_FACE_RECOGNITION=false
FRONTEND_ORIGINS=https://your-vercel-app.vercel.app
ADMIN_EMAIL=your_admin_email
ADMIN_PASSWORD=your_admin_password
```

After Render deploys, copy the API URL. It will look like:

```text
https://attendance-system-api.onrender.com
```

## Vercel Frontend

Create a Vercel project from the same GitHub repo:

- Root directory: `frontend`
- Framework preset: Vite
- Build command: `npm run build`
- Output directory: `dist`

Set this Vercel environment variable:

```env
VITE_API_URL=https://your-render-api.onrender.com
```

The `frontend/vercel.json` file is included so refresh and direct links like `/login` work.

## Final Step

After Vercel gives you the live frontend URL, update Render:

```env
FRONTEND_ORIGINS=https://your-vercel-app.vercel.app,http://localhost:5173,http://127.0.0.1:5173
```

Then redeploy the Render backend.

## Hugging Face Backend Alternative

The backend can also run on Hugging Face Spaces with Docker.

Use the included root files:

- `Dockerfile`
- `.dockerignore`
- `README.md`
- `HUGGINGFACE_DEPLOYMENT.md`

Create a Hugging Face Space with SDK `Docker`, then add the same backend environment variables as Space secrets.

The backend URL will look like:

```text
https://your-username-attendance-system-api.hf.space
```

If you use Hugging Face instead of Render, set this in Vercel:

```env
VITE_API_URL=https://your-username-attendance-system-api.hf.space
```
