# Hugging Face Backend Deployment

Use Hugging Face Spaces with Docker for the backend API.

## Create Space

1. Open Hugging Face.
2. Create a new Space.
3. Select SDK: `Docker`.
4. Set Space name: `attendance-system-api`.
5. Keep the Space public if the Vercel frontend needs to call it.

## Required Secrets

Add these in Space Settings > Variables and secrets > Secrets:

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
FRONTEND_ORIGINS=https://your-vercel-app.vercel.app,http://localhost:5173,http://127.0.0.1:5173
ADMIN_EMAIL=your_admin_email
ADMIN_PASSWORD=your_admin_password
```

## Frontend Setting

After the Space is running, set this in Vercel:

```env
VITE_API_URL=https://your-username-attendance-system-api.hf.space
```

Then redeploy Vercel.

## Notes

- Hugging Face Docker Spaces use port `7860`.
- Free CPU Spaces can sleep after inactivity, so the first request may be slow.
- Face recognition model files are downloaded into the container user's home directory when first used.
