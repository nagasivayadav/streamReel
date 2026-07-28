# StreamReel Backend

FastAPI backend for the StreamReel project — auth, video catalog, watch history,
and a basic recommendation engine.

## Run it locally with Docker (easiest)

```bash
docker-compose up --build
```

Then visit http://localhost:8000/docs for the interactive API docs (Swagger UI) —
this is the fastest way to test every endpoint without building the frontend first.

## Run it without Docker

```bash
python -m venv venv
source venv/bin/activate        # Windows: venv\Scripts\activate
pip install -r requirements.txt

# Make sure Postgres is running locally and matches DATABASE_URL in app/database.py
uvicorn app.main:app --reload
```

## Run tests

```bash
pytest
```

## Known issue already fixed for you

`passlib` 1.7.4 breaks with `bcrypt` 4.x (a version-detection bug in passlib
crashes password hashing with a misleading "password cannot be longer than 72
bytes" error, even for short passwords). This was caught by actually running
the test suite while building this, and `requirements.txt` pins `bcrypt==3.2.2`
to avoid it. If you ever upgrade bcrypt independently, this will resurface.

## Endpoints implemented

| Method | Path | Purpose |
|---|---|---|
| POST | /api/auth/signup | Create account, returns JWT |
| POST | /api/auth/login | Authenticate, returns JWT |
| GET | /api/videos | List/filter videos by genre |
| GET | /api/videos/search?q= | Search videos by title |
| GET | /api/videos/{id} | Get single video details |
| POST | /api/watch-history | Save/update playback position |
| GET | /api/watch-history/{profile_id}/{video_id} | Get resume position |
| GET | /api/recommendations/{profile_id} | Genre-based recommendations |

## What's real vs. what's still a placeholder

- Auth, hashing, JWT: **fully real**
- Video catalog / search / watch-history: **fully real**, backed by Postgres
- Recommendation engine: **real but intentionally simple** — genre-frequency based.
  Swap the logic in `app/routers/recommendation_routes.py` for a proper
  collaborative-filtering model (pandas/scikit-learn) if you want to defend
  a more advanced version in a viva.
- HLS video streaming: **not implemented here** — `hls_url` is just a stored
  string field. Actual adaptive streaming requires running video files through
  ffmpeg to produce `.m3u8` manifests, which is a separate pipeline (Member 4's
  responsibility per the project report).
- Redis: wired into `docker-compose.yml` but not yet used in code — add it for
  session storage or caching once auth/session load actually needs it.
