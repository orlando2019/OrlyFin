from __future__ import annotations

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.domains.auth_users.infrastructure.models import Organization, User


class OrganizationRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_by_slug(self, slug: str) -> Organization | None:
        return self.db.scalar(select(Organization).where(Organization.slug == slug))

    def create(self, slug: str, name: str) -> Organization:
        organization = Organization(slug=slug, name=name)
        self.db.add(organization)
        self.db.flush()
        return organization


class UserRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_by_id(self, user_id: str) -> User | None:
        return self.db.scalar(select(User).where(User.id == user_id))

    def get_by_email(self, organization_id: str, email: str) -> User | None:
        return self.db.scalar(
            select(User).where(User.organization_id == organization_id, User.email == email.lower())
        )

    def create(self, organization_id: str, email: str, full_name: str, hashed_password: str) -> User:
        user = User(
            organization_id=organization_id,
            email=email.lower(),
            full_name=full_name,
            hashed_password=hashed_password,
            is_active=True,
        )
        self.db.add(user)
        self.db.flush()
        return user
