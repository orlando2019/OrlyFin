from __future__ import annotations

from typing import Any

import jwt
from fastapi import Depends, Request
from sqlalchemy.orm import Session

from app.core.config import settings
from app.core.dependencies import get_db
from app.core.errors import AppError
from app.core.security import (
    create_access_token,
    create_refresh_token,
    decode_access_token,
    decode_refresh_token,
    hash_password,
    verify_password,
)
from app.domains.auth_users.infrastructure.repository import OrganizationRepository, UserRepository
from app.domains.rbac.application.service import RbacService
from app.domains.auth_users.infrastructure.models import User


class AuthUsersService:
    def __init__(self, db: Session):
        self.db = db
        self.org_repo = OrganizationRepository(db)
        self.user_repo = UserRepository(db)
        self.rbac_service = RbacService(db)

    def ensure_bootstrap_data(self) -> None:
        org = self.org_repo.get_by_slug(settings.bootstrap_org_slug)
        if org is None:
            org = self.org_repo.create(settings.bootstrap_org_slug, settings.bootstrap_org_name)

        admin = self.user_repo.get_by_email(org.id, settings.bootstrap_admin_email)
        if admin is None:
            admin = self.user_repo.create(
                organization_id=org.id,
                email=settings.bootstrap_admin_email,
                full_name="Owner Admin",
                hashed_password=hash_password(settings.bootstrap_admin_password),
            )
            self.rbac_service.assign_roles_to_user(admin.id, ["owner_admin"], organization_id=org.id)

        self.db.commit()

    def authenticate(self, email: str, password: str) -> tuple[User, dict[str, Any]]:
        org = self.org_repo.get_by_slug(settings.bootstrap_org_slug)
        if org is None:
            raise AppError("UNAUTHORIZED", "Invalid credentials", 401)

        user = self.user_repo.get_by_email(org.id, email)
        if not user or not verify_password(password, user.hashed_password) or not user.is_active:
            raise AppError("UNAUTHORIZED", "Invalid credentials", 401)

        roles = self.rbac_service.get_user_roles(user.id)
        permissions = self.rbac_service.get_user_permission_keys(user.id)
        claims = {"org": user.organization_id, "roles": roles}
        return user, {"roles": roles, "permissions": permissions, "claims": claims}

    def issue_token_pair(self, user: User, claims: dict[str, Any]) -> tuple[str, str]:
        access_token = create_access_token(subject=user.id, claims=claims)
        refresh_token = create_refresh_token(subject=user.id, claims={"org": user.organization_id})
        return access_token, refresh_token

    def decode_and_get_user(self, token: str, token_type: str = "access") -> User:
        try:
            payload = decode_access_token(token) if token_type == "access" else decode_refresh_token(token)
        except jwt.PyJWTError as exc:
            raise AppError("UNAUTHORIZED", "Invalid token", 401) from exc

        if payload.get("type") != token_type:
            raise AppError("UNAUTHORIZED", "Invalid token type", 401)

        user_id = payload.get("sub")
        if not user_id:
            raise AppError("UNAUTHORIZED", "Invalid token subject", 401)

        user = self.user_repo.get_by_id(user_id)
        if not user or not user.is_active:
            raise AppError("UNAUTHORIZED", "User not available", 401)

        return user

    def create_user(self, organization_id: str, email: str, full_name: str, password: str, role_names: list[str]) -> User:
        existing = self.user_repo.get_by_email(organization_id, email)
        if existing:
            raise AppError("CONFLICT", "Email already registered in organization", 409)

        user = self.user_repo.create(
            organization_id=organization_id,
            email=email,
            full_name=full_name,
            hashed_password=hash_password(password),
        )
        self.rbac_service.assign_roles_to_user(user.id, role_names, organization_id=organization_id)
        self.db.commit()
        return user


def get_auth_users_service(db: Session = Depends(get_db)) -> AuthUsersService:
    return AuthUsersService(db)


def get_current_user(
    request: Request,
    auth_service: AuthUsersService = Depends(get_auth_users_service),
) -> User:
    token = request.cookies.get(settings.jwt_access_cookie_name)
    if not token:
        raise AppError("UNAUTHORIZED", "Access token missing", 401)

    return auth_service.decode_and_get_user(token, token_type="access")
