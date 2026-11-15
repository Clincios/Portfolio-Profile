from contextlib import asynccontextmanager
from pathlib import Path

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse, PlainTextResponse, Response
from fastapi.staticfiles import StaticFiles
from starlette.middleware.sessions import SessionMiddleware

from app.admin import setup_admin
from app.config import get_settings
from app.database import Base, engine
from app.routers import auth, contact, education, experience, profile, projects, skills

# Ensure models are registered with metadata
import app.models  # noqa: F401

settings = get_settings()

FRONTEND_DIR = Path(__file__).resolve().parent.parent.parent


@asynccontextmanager
async def lifespan(_app: FastAPI):
    Base.metadata.create_all(bind=engine)
    yield


app = FastAPI(
    title="Portfolio API",
    description="Backend API for the personal portfolio website.",
    version="1.0.0",
    lifespan=lifespan,
)

app.add_middleware(
    SessionMiddleware,
    secret_key=settings.secret_key,
)
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origin_list or ["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(profile.router)
app.include_router(skills.router)
app.include_router(experience.router)
app.include_router(projects.router)
app.include_router(education.router)
app.include_router(contact.router)
app.include_router(auth.router)

setup_admin(app)


@app.get("/api/health")
def health() -> dict:
    return {"status": "ok"}


@app.get("/robots.txt", response_class=PlainTextResponse)
def robots_txt() -> str:
    base = settings.public_site_url
    return (
        "User-agent: *\n"
        "Allow: /\n"
        "\n"
        "Disallow: /admin\n"
        "Disallow: /api/\n"
        "Disallow: /docs\n"
        "Disallow: /redoc\n"
        "Disallow: /openapi.json\n"
        "\n"
        f"Sitemap: {base}/sitemap.xml\n"
    )


@app.get("/sitemap.xml")
def sitemap_xml() -> Response:
    base = settings.public_site_url
    # Single-page site: only the homepage belongs in the sitemap (hash sections are not separate URLs).
    body = (
        '<?xml version="1.0" encoding="UTF-8"?>\n'
        '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
        "  <url>\n"
        f"    <loc>{base}/</loc>\n"
        "    <changefreq>weekly</changefreq>\n"
        "    <priority>1.0</priority>\n"
        "  </url>\n"
        "</urlset>\n"
    )
    return Response(body, media_type="application/xml")


css_dir = FRONTEND_DIR / "css"
js_dir = FRONTEND_DIR / "js"
assets_dir = FRONTEND_DIR / "assets"

if css_dir.exists():
    app.mount("/css", StaticFiles(directory=str(css_dir)), name="css")
if js_dir.exists():
    app.mount("/js", StaticFiles(directory=str(js_dir)), name="js")
if assets_dir.exists():
    app.mount("/assets", StaticFiles(directory=str(assets_dir)), name="assets")


@app.get("/")
def serve_index() -> FileResponse:
    return FileResponse(FRONTEND_DIR / "index.html")
