from sqlalchemy import Integer, JSON, String, Text
from sqlalchemy.orm import Mapped, mapped_column

from app.database import Base


class Project(Base):
    __tablename__ = "projects"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    title: Mapped[str] = mapped_column(String(200), nullable=False)
    description: Mapped[str] = mapped_column(Text, nullable=False)
    category: Mapped[str] = mapped_column(String(50), nullable=False, index=True)
    tech_stack: Mapped[list] = mapped_column(JSON, nullable=False, default=list)
    image_label: Mapped[str] = mapped_column(String(200), nullable=False, default="")
    image_url: Mapped[str] = mapped_column(String(500), nullable=False, default="")
    demo_url: Mapped[str] = mapped_column(String(500), nullable=False, default="#")
    demo_label: Mapped[str] = mapped_column(String(100), nullable=False, default="Live Demo")
    source_url: Mapped[str] = mapped_column(String(500), nullable=False, default="#")
    source_label: Mapped[str] = mapped_column(String(100), nullable=False, default="Source Code")
    sort_order: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
