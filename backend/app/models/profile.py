from sqlalchemy import Integer, String, Text
from sqlalchemy.orm import Mapped, mapped_column

from app.database import Base


class Profile(Base):
    __tablename__ = "profiles"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    name: Mapped[str] = mapped_column(String(100), nullable=False)
    title: Mapped[str] = mapped_column(String(150), nullable=False)
    tagline: Mapped[str] = mapped_column(String(255), nullable=False, default="")
    bio_heading: Mapped[str] = mapped_column(String(255), nullable=False, default="")
    bio_paragraph_1: Mapped[str] = mapped_column(Text, nullable=False, default="")
    bio_paragraph_2: Mapped[str] = mapped_column(Text, nullable=False, default="")
    email: Mapped[str] = mapped_column(String(255), nullable=False)
    location: Mapped[str] = mapped_column(String(150), nullable=False, default="")
    resume_url: Mapped[str] = mapped_column(String(500), nullable=False, default="#")
    github_url: Mapped[str] = mapped_column(String(500), nullable=False, default="")
    linkedin_url: Mapped[str] = mapped_column(String(500), nullable=False, default="")
    twitter_url: Mapped[str] = mapped_column(String(500), nullable=False, default="")
    typing_roles: Mapped[str] = mapped_column(
        String(500),
        nullable=False,
        default="Software Engineer,Full-Stack Developer,Cloud Architect,Engineering Lead",
    )
    years_experience: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    projects_shipped: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    teams_led: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    initials: Mapped[str] = mapped_column(String(10), nullable=False, default="")
    contact_heading: Mapped[str] = mapped_column(String(255), nullable=False, default="")
    contact_text: Mapped[str] = mapped_column(Text, nullable=False, default="")
