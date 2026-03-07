from __future__ import annotations

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.domains.auth_users.infrastructure.models import Organization, User


# Modela la responsabilidad de 'organization repository' dentro del dominio o capa actual.
class OrganizationRepository:
    # Inicializa la instancia y prepara las dependencias necesarias para sus operaciones.
    def __init__(self, db: Session):
        self.db = db

    # Obtiene 'by slug' y lo expone para su uso en la capa llamadora.
    def get_by_slug(self, slug: str) -> Organization | None:
        return self.db.scalar(select(Organization).where(Organization.slug == slug))

    # Ejecuta la lógica principal de 'create' y devuelve el resultado esperado por el flujo.
    def create(self, slug: str, name: str) -> Organization:
        organization = Organization(slug=slug, name=name)
        self.db.add(organization)
        self.db.flush()
        return organization


# Modela la responsabilidad de 'user repository' dentro del dominio o capa actual.
class UserRepository:
    # Inicializa la instancia y prepara las dependencias necesarias para sus operaciones.
    def __init__(self, db: Session):
        self.db = db

    # Obtiene 'by id' y lo expone para su uso en la capa llamadora.
    def get_by_id(self, user_id: str) -> User | None:
        return self.db.scalar(select(User).where(User.id == user_id))

    # Obtiene 'by email' y lo expone para su uso en la capa llamadora.
    def get_by_email(self, organization_id: str, email: str) -> User | None:
        return self.db.scalar(
            select(User).where(User.organization_id == organization_id, User.email == email.lower())
        )

    # Ejecuta la lógica principal de 'create' y devuelve el resultado esperado por el flujo.
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
