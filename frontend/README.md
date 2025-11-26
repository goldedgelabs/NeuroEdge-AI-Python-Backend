# NeuroEdge Frontend - Final Build (Mode A)

This package contains the NeuroEdge frontend (production-ready subset), built for deployment.

## Quickstart

1. Place this `/frontend` folder into your `/neuroedge` monorepo.
2. Create `.env.local` in `frontend/` with:
   NEXT_PUBLIC_TS_BACKEND=http://your-ts-backend:4000
   NEXT_PUBLIC_PY_BACKEND=http://your-py-backend:5000
   NEXT_PUBLIC_GO_BACKEND=http://your-go-backend:6000

3. Install:
   ```
   cd frontend
   npm ci
   ```

4. Dev:
   ```
   npm run dev
   ```

5. Build:
   ```
   npm run build
   npm run start
   ```

## Deploy

- Use Dockerfile and top-level docker-compose.yml (included) to run locally.
- For Cloudflare Pages + Worker, adapt `worker/` files and deploy via `wrangler`.

## Notes
- No node_modules included. Run `npm ci` before running.
- Durable Object and Worker examples need Cloudflare bindings configured.
- Playwright tests are included under `frontend/tests/e2e`.
