# Deploying THE TEACHKIT

This covers what's needed to get the merged app (`backend/` FastAPI + `frontend/` React) live at **theteachkit.com**. Everything in this doc is prep — actually creating accounts, deploying, and changing DNS needs your credentials and is a real, externally-visible action, so that part is on you (or ask me to walk through a specific step live).

## What's already built

- `backend/Dockerfile`, `backend/.dockerignore`, `backend/requirements.txt` (trimmed to actual runtime deps) — the API is container-ready.
- `frontend/Dockerfile` (multi-stage Yarn build → nginx), `frontend/nginx.conf` (SPA routing fallback), `frontend/.dockerignore` — same for the frontend, if you want to self-host it rather than use a static-site host.
- `docker-compose.yml` at the project root — spins up a real MongoDB + the backend + the frontend together for local full-stack testing (better than the in-memory mongomock harness used for one-off checks during development). Run with:
  ```bash
  docker compose up --build
  ```
  (Needs Docker Desktop installed — it wasn't available in the environment I was working in, so I wasn't able to actually run a build myself; worth a local test run before you deploy anywhere.)

## Environment variables

**Backend** (`backend/.env` locally; set as real secrets in your host's dashboard for production — never commit `.env`):

| Variable | Required | Notes |
|---|---|---|
| `MONGO_URL` | yes | Connection string. For production, a MongoDB Atlas free/shared cluster is the easiest path — self-hosting Mongo is more ops work than this app needs at this scale. |
| `DB_NAME` | yes | e.g. `theteachkit_prod` |
| `JWT_SECRET` | yes | Generate a long random string — `python3 -c "import secrets; print(secrets.token_hex(32))"` |
| `ANTHROPIC_API_KEY` | yes | You already have a dedicated TeachKit key (currently in `backend/.env` locally). |
| `JWT_ALGORITHM` | no | Defaults to `HS256`. |
| `CORS_ORIGINS` | recommended | Defaults to `*` — for production, set this to `https://theteachkit.com` (and any staging URL) so the API only accepts requests from your actual frontend. |

**Frontend** (baked in at build time, per Create React App convention):

| Variable | Required | Notes |
|---|---|---|
| `REACT_APP_BACKEND_URL` | yes | The backend's public URL, e.g. `https://api.theteachkit.com`. Must be set *before* `yarn build` runs — changing it after build requires a rebuild, not just a restart. |

## Hosting recommendation

The backend needs a real persistent process (not serverless functions) plus a MongoDB connection — this rules out Netlify/Vercel for the backend specifically (see the earlier note on this). Recommended split:

- **Backend + MongoDB**: [Render](https://render.com) — supports Docker deploys directly from this `backend/Dockerfile`, has a managed Postgres/Redis but for Mongo you'd pair it with **MongoDB Atlas** (generous free tier, minutes to set up, works from anywhere). Railway or Fly.io are equally reasonable alternatives if you already have a preference.
- **Frontend**: **Netlify or Vercel** — this part genuinely is a great fit for either, since it's a static React build with no server-side logic. Point it at `frontend/`, build command `yarn build`, publish directory `build/`, and set `REACT_APP_BACKEND_URL` as a build-time environment variable in their dashboard. (You don't need `frontend/Dockerfile`/`nginx.conf` at all if you go this route — those are only for self-hosting the frontend yourself instead.)

This mirrors how your local engine already uses Netlify successfully — just for the frontend half here, with a proper backend host for the FastAPI/Mongo half instead of trying to force serverless functions to do something they're not built for.

## Suggested rollout order

1. **MongoDB Atlas**: create a free cluster, get the connection string.
2. **Backend**: deploy `backend/` (via Dockerfile) to Render/Railway/Fly, set all the env vars above, confirm `GET /api/` returns `{"message": "THE TEACHKIT API is running", ...}`.
3. **Frontend**: deploy `frontend/` to Netlify/Vercel with `REACT_APP_BACKEND_URL` pointed at the backend's real URL from step 2.
4. **Validate on the host's default URLs first** (e.g. `your-app.onrender.com`, `your-app.netlify.app`) — full signup → onboarding → generate → enrich → export flow, for real, before touching DNS.
5. **DNS for theteachkit.com**: once step 4 is solid, point the domain at your frontend host (CNAME/A record per their instructions) and optionally a subdomain like `api.theteachkit.com` at the backend. Leave `teachkit.emergent.host` (the current contest submission) untouched until this is fully validated and ready to replace it.

## What I can't do myself

Creating hosting/Atlas accounts, entering payment details, deploying to your infrastructure, and changing DNS records for a domain you own are all real, externally-visible, and in some cases costly actions — outside what I'll do without you directly driving them. Happy to walk through any specific step with you live, or troubleshoot if something doesn't come up right after you deploy.
