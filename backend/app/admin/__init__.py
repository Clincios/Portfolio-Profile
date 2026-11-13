from sqladmin import Admin, ModelView
from sqladmin.authentication import AuthenticationBackend
from starlette.requests import Request

from app.config import get_settings
from app.database import SessionLocal, engine
from app.models import (
    ContactMessage,
    Education,
    Experience,
    Profile,
    Project,
    Skill,
    SkillCategory,
    User,
)
from app.services.auth import authenticate_user


class AdminAuth(AuthenticationBackend):
    async def login(self, request: Request) -> bool:
        form = await request.form()
        username = str(form.get("username", ""))
        password = str(form.get("password", ""))
        db = SessionLocal()
        try:
            user = authenticate_user(db, username, password)
            if not user:
                return False
            request.session.update({"admin_user": user.username})
            return True
        finally:
            db.close()

    async def logout(self, request: Request) -> bool:
        request.session.clear()
        return True

    async def authenticate(self, request: Request) -> bool:
        return bool(request.session.get("admin_user"))


class UserAdmin(ModelView, model=User):
    column_list = [User.id, User.username, User.is_active]
    column_searchable_list = [User.username]
    form_excluded_columns = [User.hashed_password]
    can_create = False
    name = "User"
    name_plural = "Users"
    icon = "fa-solid fa-user"


class ProfileAdmin(ModelView, model=Profile):
    column_list = [Profile.id, Profile.name, Profile.title, Profile.email, Profile.location]
    column_searchable_list = [Profile.name, Profile.email]
    name = "Profile"
    name_plural = "Profiles"
    icon = "fa-solid fa-id-card"


class SkillCategoryAdmin(ModelView, model=SkillCategory):
    column_list = [SkillCategory.id, SkillCategory.title, SkillCategory.icon, SkillCategory.sort_order]
    name = "Skill Category"
    name_plural = "Skill Categories"
    icon = "fa-solid fa-layer-group"


class SkillAdmin(ModelView, model=Skill):
    column_list = [Skill.id, Skill.name, Skill.category_id, Skill.sort_order]
    name = "Skill"
    name_plural = "Skills"
    icon = "fa-solid fa-code"


class ExperienceAdmin(ModelView, model=Experience):
    column_list = [
        Experience.id,
        Experience.role,
        Experience.company,
        Experience.date_range,
        Experience.sort_order,
    ]
    name = "Experience"
    name_plural = "Experience"
    icon = "fa-solid fa-briefcase"


class ProjectAdmin(ModelView, model=Project):
    column_list = [
        Project.id,
        Project.title,
        Project.category,
        Project.sort_order,
    ]
    column_searchable_list = [Project.title, Project.category]
    name = "Project"
    name_plural = "Projects"
    icon = "fa-solid fa-folder-open"


class EducationAdmin(ModelView, model=Education):
    column_list = [Education.id, Education.degree, Education.school, Education.year, Education.sort_order]
    name = "Education"
    name_plural = "Education"
    icon = "fa-solid fa-graduation-cap"


class ContactMessageAdmin(ModelView, model=ContactMessage):
    column_list = [
        ContactMessage.id,
        ContactMessage.name,
        ContactMessage.email,
        ContactMessage.subject,
        ContactMessage.is_read,
        ContactMessage.created_at,
    ]
    column_searchable_list = [ContactMessage.name, ContactMessage.email, ContactMessage.subject]
    column_default_sort = [(ContactMessage.created_at, True)]
    can_create = False
    name = "Contact Message"
    name_plural = "Contact Messages"
    icon = "fa-solid fa-envelope"


def setup_admin(app) -> Admin:
    settings = get_settings()
    authentication_backend = AdminAuth(secret_key=settings.secret_key)
    admin = Admin(
        app,
        engine,
        authentication_backend=authentication_backend,
        title="Portfolio Admin",
    )
    admin.add_view(ProfileAdmin)
    admin.add_view(SkillCategoryAdmin)
    admin.add_view(SkillAdmin)
    admin.add_view(ExperienceAdmin)
    admin.add_view(ProjectAdmin)
    admin.add_view(EducationAdmin)
    admin.add_view(ContactMessageAdmin)
    admin.add_view(UserAdmin)
    return admin
