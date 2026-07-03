# AI Insurance Portal (Monorepo)

This repository contains both the frontend (Angular) and the backend (FastAPI) for the AI Insurance Portal.

## Project Structure

- `/frontend` - Angular 17+ client (uses Angular Signals and Zoneless change detection)
- `/backend` - FastAPI server with OpenAI (gpt-4o-mini) and SQL database

---

## How to Deploy

### 1. Backend (Deploy on Render)

1. Create a free account on [Render](https://render.com/).
2. Click **New +** and select **Blueprint** (or **Web Service**).
3. Connect your GitHub repository.
4. If using **Blueprint**, Render will read `render.yaml` automatically.
5. If creating a **Web Service** manually, use these configurations:
   - **Environment**: `Python`
   - **Root Directory**: `backend`
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `uvicorn app.main:app --host 0.0.0.0 --port $PORT`
6. Add the following **Environment Variables**:
   - `PYTHON_VERSION`: `3.11.0`
   - `SECRET_KEY`: `your_jwt_secret_key`
   - `DATABASE_URL`: `sqlite:///insurance.db` (or a PostgreSQL connection string)
   - `OPENAI_API_KEY`: `your_openai_api_key`

---

### 2. Frontend (Deploy on Vercel)

1. Create a free account on [Vercel](https://vercel.com/).
2. Click **Add New** and choose **Project**.
3. Import your GitHub repository.
4. In the configuration settings:
   - **Framework Preset**: Choose `Angular`
   - **Root Directory**: Click Edit and select the `frontend` folder
   - **Build and Output Settings**: Leave as default (`npm run build`)
5. Click **Deploy**. Vercel will automatically detect the configuration and publish the app.

---

## Local Development

### Run Backend
```bash
cd backend
uv run uvicorn app.main:app --reload
```

### Run Frontend
```bash
cd frontend
npm run start
```
