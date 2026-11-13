from datetime import datetime
from typing import List, Optional

from pydantic import BaseModel, ConfigDict, EmailStr, Field


class ProfileOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    name: str
    title: str
    tagline: str
    bio_heading: str
    bio_paragraph_1: str
    bio_paragraph_2: str
    email: str
    location: str
    resume_url: str
    github_url: str
    linkedin_url: str
    twitter_url: str
    typing_roles: str
    years_experience: int
    projects_shipped: int
    teams_led: int
    initials: str
    contact_heading: str
    contact_text: str


class SkillOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    name: str
    sort_order: int


class SkillCategoryOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    title: str
    icon: str
    sort_order: int
    skills: List[SkillOut] = []


class ExperienceOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    date_range: str
    role: str
    company: str
    details: List[str]
    sort_order: int


class ProjectOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    title: str
    description: str
    category: str
    tech_stack: List[str]
    image_label: str
    image_url: str
    demo_url: str
    demo_label: str
    source_url: str
    source_label: str
    sort_order: int


class EducationOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    degree: str
    school: str
    year: str
    sort_order: int


class ContactCreate(BaseModel):
    name: str = Field(..., min_length=1, max_length=100)
    email: EmailStr
    subject: str = Field(..., min_length=1, max_length=200)
    message: str = Field(..., min_length=1, max_length=5000)


class ContactResponse(BaseModel):
    success: bool
    message: str


class ContactMessageOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    name: str
    email: str
    subject: str
    message: str
    is_read: bool
    created_at: datetime


class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"


class LoginRequest(BaseModel):
    username: str
    password: str


class UserOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    username: str
    is_active: bool
