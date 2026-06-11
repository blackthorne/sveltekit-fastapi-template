# SvelteKit + FastAPI Template

A minimal full-stack template:

- **Frontend**: SvelteKit 2 / Svelte 5 (runes), built as a pure SPA with `adapter-static`
- **Styling**: Pico CSS 2 (classless-friendly, dark mode automatic)
- **Backend**: FastAPI with JWT auth (PyJWT + bcrypt)
- **Desktop-ready**: the frontend builds to plain static files, so it can be wrapped with Tauri 2 with no architectural changes

```
.
├── docker-compose.yml
├── frontend/   SvelteKit SPA (+ Dockerfile, nginx.conf)
└── backend/    FastAPI API  (+ Dockerfile)
```

## Quick start

### Backend

```bash
cd backend
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env        # then change SECRET_KEY
uvicorn app.main:app --reload --port 8000
```

API docs at http://localhost:8000/docs. A demo user `demo` / `demo1234` is seeded on startup.

### Frontend

```bash
cd frontend
npm install
cp .env.example .env
npm run dev
```

Open http://localhost:5173.

### Or run everything with Docker

```bash
docker compose up --build
```

- Frontend: http://localhost:3000 (nginx serving the static SPA build)
- Backend: http://localhost:8000 (docs at `/docs`)

Override secrets/config via a `.env` file next to `docker-compose.yml` (e.g. `SECRET_KEY=...`, `VITE_API_URL=...`). Note that `VITE_API_URL` is baked in at **build** time (Vite inlines env vars) and must be the URL the *browser* uses to reach the API — `http://localhost:8000` for local use, your public API URL when deploying. Changing it requires `docker compose build frontend`.

## How auth works

1. `POST /auth/login` with JSON `{username, password}` returns `{access_token}` (HS256 JWT, `sub` = username).
2. The frontend stores the token in `localStorage` and sends it as `Authorization: Bearer <token>` (see `frontend/src/lib/api.js`).
3. Protected endpoints depend on `CurrentUser` (`backend/app/auth.py`), which validates the token and loads the user.
4. On 401, the frontend clears the token and redirects to `/login`.

The user store is in-memory (`backend/app/users.py`) so the template runs with zero setup — replace its four functions with a real database (SQLModel/SQLAlchemy) when you build on this.

**Production notes**: set a real `SECRET_KEY`, shorten `ACCESS_TOKEN_EXPIRE_MINUTES`, serve over HTTPS, and consider refresh-token rotation if you need long-lived sessions. `localStorage` is the pragmatic choice here because httpOnly cookies don't play well with Tauri's custom-protocol origin; if you stay web-only and want cookie-based auth, that's a reasonable swap.

## Why this is Tauri-compatible

Three decisions in the frontend make the Tauri conversion trivial:

1. **`adapter-static` with `fallback: 'index.html'`** (`svelte.config.js`) — the build output is plain HTML/JS/CSS, no Node server.
2. **`ssr = false`** in the root `+layout.js` — nothing depends on server-side rendering.
3. **Absolute API URL** via `VITE_API_URL` — the app never assumes the API is same-origin, which it won't be inside a Tauri webview.

The backend's CORS config already allows the Tauri origins (`tauri://localhost` for macOS/Linux, `http://tauri.localhost` for Windows).

## Converting to a desktop app with Tauri 2

Prerequisites: Rust toolchain + platform deps (https://v2.tauri.app/start/prerequisites/).

```bash
cd frontend
npm install -D @tauri-apps/cli
npx tauri init
```

Answer the prompts (or edit `src-tauri/tauri.conf.json` afterwards) with:

| Prompt | Value |
|---|---|
| Web assets location (`frontendDist`) | `../build` |
| Dev server URL (`devUrl`) | `http://localhost:5173` |
| Frontend dev command (`beforeDevCommand`) | `npm run dev` |
| Frontend build command (`beforeBuildCommand`) | `npm run build` |

Then:

```bash
npx tauri dev     # desktop app against the Vite dev server
npx tauri build   # production bundle (.app/.dmg/.msi/.deb/...)
```

For a production desktop app, point `VITE_API_URL` at your deployed API (set it in `.env.production` or at build time: `VITE_API_URL=https://api.example.com npm run build`).

Optional hardening for desktop: move the JWT from `localStorage` into the OS keychain via a Tauri plugin (e.g. keyring/stronghold), and restrict the Tauri capability/permissions config to only what the app needs.

## Stack versions (verified June 2026)

| Package | Version |
|---|---|
| @sveltejs/kit | ^2.65 |
| svelte | ^5.56 |
| @sveltejs/adapter-static | ^3.0 |
| vite | ^8.0 |
| @picocss/pico | ^2.1 |
| fastapi | ≥0.136 |
| pyjwt | ≥2.13 |
| bcrypt | ≥5.0 |
| Tauri (optional) | 2.x |
