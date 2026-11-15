# Clinton Age — Senior Software Engineer Portfolio

A modern, responsive, single-page portfolio website with a **FastAPI** backend, SQLite/PostgreSQL storage, contact form handling, and an admin panel for managing content.

## Features

- **Responsive Design** — Looks great on desktop, tablet, and mobile.
- **Dark/Light Theme** — Toggle theme with `localStorage` persistence.
- **Smooth Navigation** — Sticky header, smooth scroll, and active section highlighting.
- **Interactive Elements** — Typing effect, scroll-reveal animations, animated counters, and project filtering.
- **Accessible** — Semantic HTML, ARIA labels, keyboard focus states, and reduced-motion support.
- **Contact Form** — Client-side validation plus server-side API submission (stored in DB, optional email).
- **Dynamic Content API** — Profile, skills, experience, projects, and education loaded from the backend.
- **Admin Panel** — SQLAdmin UI at `/admin` for CRUD on all content and contact messages.

## Project Structure

```
Website-project/
├── index.html              # Main page
├── css/
│   └── styles.css          # All styles and themes
├── js/
│   ├── config.js           # API base URL
│   ├── api.js              # Fetch wrappers
│   ├── content.js          # Load & render dynamic content
│   ├── theme.js            # Dark/light mode toggle
│   ├── navigation.js       # Mobile menu, smooth scroll, active link
│   ├── animations.js       # Scroll reveal, typing effect, counters
│   └── main.js             # Project filters, contact form, footer year
├── assets/
│   └── images/             # Add your profile photo and project screenshots here
├── backend/
│   ├── app/                # FastAPI application
│   ├── alembic/            # Database migrations
│   ├── scripts/seed.py     # Seed sample content + admin user
│   ├── requirements.txt
│   └── .env.example
├── docker-compose.yml      # Optional PostgreSQL + backend
└── README.md
```

## How to Run Locally (with Backend)

```bash
cd backend
python -m venv venv
venv\Scripts\activate          # Windows
# source venv/bin/activate     # macOS / Linux

pip install -r requirements.txt
copy .env.example .env         # Windows
# cp .env.example .env         # macOS / Linux

alembic upgrade head
python -m scripts.seed
uvicorn app.main:app --reload --port 8000
```

Then open:

- Site: [http://localhost:8000](http://localhost:8000)
- API docs: [http://localhost:8000/docs](http://localhost:8000/docs)
- Admin: [http://localhost:8000/admin](http://localhost:8000/admin) — default `admin` / `changeme`

## Static-Only Preview

You can still open `index.html` directly or serve static files without the backend. Dynamic API sections will keep the hardcoded markup as a fallback.

```bash
python -m http.server 8000
# or: npx serve
```

If the static server is separate from the API, set the API base URL before other scripts:

```html
<script>window.__API_BASE_URL__ = 'http://localhost:8000';</script>
```

## API Overview

| Method | Path | Description |
|--------|------|-------------|
| GET | `/api/profile` | Hero + about content |
| GET | `/api/skills` | Skill categories with skills |
| GET | `/api/experience` | Experience timeline |
| GET | `/api/projects` | Projects (`?category=` optional) |
| GET | `/api/education` | Education entries |
| POST | `/api/contact` | Submit contact form |
| POST | `/api/auth/login` | Admin JWT (OAuth2 form) |
| GET | `/api/auth/me` | Current admin user |

## Customization

1. **Content** — Prefer the admin panel at `/admin`, or edit seed data and re-run `python -m scripts.seed` on a fresh DB.
2. **Colors** — Update CSS variables at the top of `css/styles.css`.
3. **Images** — Add files under `assets/images/` and set URLs in the admin panel. Add a `1200×630` `assets/images/og-image.jpg` for social / Google previews.
4. **Resume** — Set `resume_url` on the Profile record.
5. **Email** — Configure SMTP variables in `backend/.env` to receive contact notifications.
6. **SEO domain** — Live site: `https://portfolio-profile-p56d.onrender.com`. Keep `SITE_URL` on Render matched to that origin (or your custom domain later).

## SEO, Search Console & Google Business Profile

### On the site (already wired)

- Meta title/description, canonical, Open Graph, Twitter cards, robots directives
- JSON-LD for `Person`, `ProfessionalService`, and `WebSite`
- `robots.txt` + `sitemap.xml` (served dynamically when FastAPI runs; static copies at repo root)
- Services section + copy aimed at **your name** and **web development** searches

### After you deploy

1. Point a custom domain at your host (stronger for branding than `*.onrender.com`).
2. Set `SITE_URL=https://portfolio-profile-p56d.onrender.com` on Render (already the code default).
3. Confirm [robots.txt](https://portfolio-profile-p56d.onrender.com/robots.txt) and [sitemap.xml](https://portfolio-profile-p56d.onrender.com/sitemap.xml) load.
4. Upload `assets/images/og-image.jpg` (1200×630) with your name readable on it.

### Google Search Console

1. Open [Google Search Console](https://search.google.com/search-console) → **Add property** → Domain (preferred) or URL-prefix.
2. Verify ownership (DNS TXT for domain, or HTML meta / file for URL-prefix).
3. **Sitemaps** → submit `https://your-domain.com/sitemap.xml`.
4. Use **URL Inspection** on the homepage → **Request indexing**.
5. Track queries for your name and “web developer” / “web development” + your city over the next weeks.

### Google Business Profile (local visibility)

1. Create/claim a profile at [Google Business Profile](https://business.google.com) (or Google Maps → Add your business).
2. Category ideas: **Website designer**, **Software company**, or **Internet marketing service** (pick the closest match; add secondary categories if offered).
3. If you work from home / remotely: set as a **service-area business**, hide the street address if needed, and list cities you serve.
4. Website field → your live portfolio URL. Keep name consistent with the site (**Clinton Age** / your legal business name).
5. Add services matching the site (Custom website development, Full-stack web apps, etc.), hours, phone, and photos.
6. Complete verification (postcard, phone, or email—Google’s flow varies).
7. Ask happy clients for Google reviews; reply to every review.

### Ongoing ranking tips

- Keep LinkedIn / GitHub / other profiles linking to the same domain and spelling of your name.
- Publish real projects with unique titles/descriptions (admin panel).
- Avoid stuffing keywords; keep one clear H1 with your name (already set).
- After major content changes, re-request indexing in Search Console.

## Docker (PostgreSQL)

```bash
docker compose up --build
```

## Deployment

- **Backend + frontend together (recommended):** Deploy the FastAPI app (e.g. Railway, Render, Fly.io) — it serves static files and the API.
- **Static hosting only:** Host HTML/CSS/JS on Netlify/Vercel/Cloudflare Pages and point `__API_BASE_URL__` at your API; set `CORS_ORIGINS` accordingly.
- Use PostgreSQL in production via `DATABASE_URL` and set a strong `SECRET_KEY` and `ADMIN_PASSWORD`.

### Deploy on Render (monolith)

This repo includes `render.yaml` (Web Service + Postgres) and a Docker build that serves the site and API together.

1. Push this project to GitHub or GitLab.
2. In the [Render Dashboard](https://dashboard.render.com): **New** → **Blueprint** → connect the repo.
3. When prompted for sync’d env vars, set:
   - `ADMIN_PASSWORD` — strong password for `/admin`
   - `CORS_ORIGINS` — leave blank for the first deploy, then set to `https://<your-service>.onrender.com` and redeploy (or update after the URL is assigned)
   - `SITE_URL` — same public origin, e.g. `https://<your-service>.onrender.com` or your custom domain (used by `/sitemap.xml` and `/robots.txt`)
   - `DATABASE_URL` is injected from the Blueprint Postgres service; paste Render’s URL as-is (`postgres://` or `postgresql://`) — the app rewrites it to `postgresql+psycopg2://`
4. After deploy, open:
   - Site: `https://<your-service>.onrender.com`
   - Health: `/api/health`
   - Admin: `/admin` (username defaults to `admin` unless you change `ADMIN_USERNAME`)
5. Optional: add SMTP env vars (`MAIL_*`) for contact-form email; messages are always stored in the database.

Manual alternative (no Blueprint): create a **PostgreSQL** database, then a **Web Service** with Docker, Dockerfile path `backend/Dockerfile`, context `.`, and the same env vars (`DATABASE_URL` from the database, `SECRET_KEY`, `ADMIN_*`, `CORS_ORIGINS`).

## Browser Support

Modern evergreen browsers (Chrome, Firefox, Safari, Edge).

## License

This project is provided as a starting template for your personal portfolio. Feel free to modify and use it as you like.
