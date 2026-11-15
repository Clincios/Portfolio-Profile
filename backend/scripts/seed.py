"""Seed the database with portfolio content from the original static site."""

from __future__ import annotations

import sys
from pathlib import Path

# Allow running as `python -m scripts.seed` from the backend directory.
BACKEND_ROOT = Path(__file__).resolve().parent.parent
if str(BACKEND_ROOT) not in sys.path:
    sys.path.insert(0, str(BACKEND_ROOT))

from app.config import get_settings
from app.database import Base, SessionLocal, engine
from app.models import (
    Education,
    Experience,
    Profile,
    Project,
    Skill,
    SkillCategory,
    User,
)
from app.services.auth import get_password_hash


def seed() -> None:
    settings = get_settings()
    Base.metadata.create_all(bind=engine)
    db = SessionLocal()

    try:
        if not db.query(User).filter(User.username == settings.admin_username).first():
            db.add(
                User(
                    username=settings.admin_username,
                    hashed_password=get_password_hash(settings.admin_password),
                    is_active=True,
                )
            )
            print(f"Created admin user: {settings.admin_username}")
        else:
            print("Admin user already exists; skipping.")

        if not db.query(Profile).first():
            db.add(
                Profile(
                    name="Clinton Age",
                    title="Web Developer & Full-Stack Software Engineer",
                    tagline=(
                        "I help businesses and founders with custom web development—fast, "
                        "scalable websites and full-stack applications people rely on every day."
                    ),
                    bio_heading="Web developer & full-stack engineer with 10+ years of experience",
                    bio_paragraph_1=(
                        "I'm Clinton Age, a web developer who designs and builds websites and "
                        "large-scale web applications that are fast, reliable, and maintainable. "
                        "My work spans the full stack—responsive frontends, robust APIs, cloud "
                        "infrastructure, and CI/CD—so you get one partner from idea to launch."
                    ),
                    bio_paragraph_2=(
                        "I've led engineering teams at startups and enterprises, mentored "
                        "developers, and partnered with product and design to ship features users "
                        "love. Whether you need a marketing site, a SaaS product, or a system "
                        "rebuild, I care about code quality, clear architecture, and results you "
                        "can measure."
                    ),
                    email="alex.morgan@example.com",
                    location="San Francisco, CA",
                    resume_url="#",
                    github_url="https://github.com",
                    linkedin_url="https://linkedin.com",
                    twitter_url="https://twitter.com",
                    typing_roles=(
                        "Web Developer,Full-Stack Developer,Software Engineer,Cloud Architect"
                    ),
                    years_experience=10,
                    projects_shipped=50,
                    teams_led=8,
                    initials="CA",
                    contact_heading="Hire me for web development",
                    contact_text=(
                        "Need a website, web app, or technical partner? Tell me about your "
                        "project—I'll reply with next steps and how we can work together."
                    ),
                )
            )
            print("Created profile.")
        else:
            print("Profile already exists; skipping.")

        if db.query(SkillCategory).count() == 0:
            categories = [
                (
                    "Languages",
                    "💻",
                    0,
                    ["JavaScript / TypeScript", "Python", "Go", "Java", "SQL"],
                ),
                (
                    "Frontend",
                    "⚛",
                    1,
                    [
                        "React / Next.js",
                        "Vue.js",
                        "HTML5 / CSS3",
                        "Tailwind CSS",
                        "Accessibility (a11y)",
                    ],
                ),
                (
                    "Backend",
                    "🖥",
                    2,
                    [
                        "Node.js / Express",
                        "GraphQL / REST",
                        "PostgreSQL / MongoDB",
                        "Redis",
                        "Kafka",
                    ],
                ),
                (
                    "Cloud & DevOps",
                    "☁",
                    3,
                    [
                        "AWS / GCP",
                        "Docker / Kubernetes",
                        "Terraform",
                        "GitHub Actions",
                        "Monitoring & Observability",
                    ],
                ),
            ]
            for title, icon, sort_order, skills in categories:
                category = SkillCategory(title=title, icon=icon, sort_order=sort_order)
                db.add(category)
                db.flush()
                for skill_order, skill_name in enumerate(skills):
                    db.add(
                        Skill(
                            category_id=category.id,
                            name=skill_name,
                            sort_order=skill_order,
                        )
                    )
            print("Created skill categories and skills.")
        else:
            print("Skills already exist; skipping.")

        if db.query(Experience).count() == 0:
            experiences = [
                Experience(
                    date_range="2021 — Present",
                    role="Staff Software Engineer",
                    company="TechCorp",
                    details=[
                        "Lead architecture for a microservices platform serving 10M+ daily users.",
                        "Reduced API latency by 40% through caching strategies and query optimization.",
                        "Mentored a team of 12 engineers and established code review and CI/CD best practices.",
                    ],
                    sort_order=0,
                ),
                Experience(
                    date_range="2017 — 2021",
                    role="Senior Software Engineer",
                    company="StartupXYZ",
                    details=[
                        "Built the core product from prototype to Series B, growing the user base to 2M.",
                        "Designed real-time data pipelines processing 1B+ events per month.",
                        "Led migration from monolith to containerized services on AWS.",
                    ],
                    sort_order=1,
                ),
                Experience(
                    date_range="2014 — 2017",
                    role="Software Engineer",
                    company="Enterprise Solutions Inc.",
                    details=[
                        "Developed customer-facing dashboards and internal tooling used by 500+ employees.",
                        "Implemented automated testing suites that reduced regression bugs by 60%.",
                        "Collaborated with product managers to define technical roadmaps.",
                    ],
                    sort_order=2,
                ),
            ]
            db.add_all(experiences)
            print("Created experience entries.")
        else:
            print("Experience already exists; skipping.")

        if db.query(Project).count() == 0:
            projects = [
                Project(
                    title="Scalable E-Commerce Platform",
                    description=(
                        "A high-performance online marketplace with real-time inventory, "
                        "payments, and analytics."
                    ),
                    category="web",
                    tech_stack=["React", "Node.js", "PostgreSQL", "AWS"],
                    image_label="E-Commerce Platform",
                    demo_url="#",
                    demo_label="Live Demo",
                    source_url="#",
                    source_label="Source Code",
                    sort_order=0,
                ),
                Project(
                    title="Real-Time Data Pipeline",
                    description=(
                        "Event streaming infrastructure handling billions of events "
                        "with sub-second latency."
                    ),
                    category="cloud",
                    tech_stack=["Go", "Kafka", "Kubernetes", "Terraform"],
                    image_label="Data Pipeline",
                    demo_url="#",
                    demo_label="Case Study",
                    source_url="#",
                    source_label="Source Code",
                    sort_order=1,
                ),
                Project(
                    title="Open Source Dev CLI",
                    description=(
                        "A command-line tool that automates common development "
                        "workflows and deployments."
                    ),
                    category="open",
                    tech_stack=["TypeScript", "Node.js", "GitHub Actions"],
                    image_label="Dev CLI Tool",
                    demo_url="#",
                    demo_label="Documentation",
                    source_url="#",
                    source_label="Source Code",
                    sort_order=2,
                ),
                Project(
                    title="Analytics SaaS Dashboard",
                    description=(
                        "Interactive dashboards and reporting tools for enterprise customers."
                    ),
                    category="web",
                    tech_stack=["Next.js", "D3.js", "GraphQL", "Docker"],
                    image_label="SaaS Dashboard",
                    demo_url="#",
                    demo_label="Live Demo",
                    source_url="#",
                    source_label="Source Code",
                    sort_order=3,
                ),
            ]
            db.add_all(projects)
            print("Created projects.")
        else:
            print("Projects already exist; skipping.")

        if db.query(Education).count() == 0:
            education_items = [
                Education(
                    degree="M.S. Computer Science",
                    school="Stanford University",
                    year="2012 — 2014",
                    sort_order=0,
                ),
                Education(
                    degree="B.S. Software Engineering",
                    school="MIT",
                    year="2008 — 2012",
                    sort_order=1,
                ),
                Education(
                    degree="AWS Certified Solutions Architect",
                    school="Amazon Web Services",
                    year="2022",
                    sort_order=2,
                ),
                Education(
                    degree="Certified Kubernetes Administrator",
                    school="Cloud Native Computing Foundation",
                    year="2021",
                    sort_order=3,
                ),
            ]
            db.add_all(education_items)
            print("Created education entries.")
        else:
            print("Education already exists; skipping.")

        db.commit()
        print("Seed completed successfully.")
    except Exception:
        db.rollback()
        raise
    finally:
        db.close()


if __name__ == "__main__":
    seed()
