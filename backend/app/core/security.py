from __future__ import annotations

from dataclasses import dataclass

from app.core.config import settings


@dataclass(frozen=True)
class JwtCookiePolicy:
    access_token_minutes: int
    refresh_token_days: int
    secure: bool
    samesite: str
    domain: str


jwt_cookie_policy = JwtCookiePolicy(
    access_token_minutes=settings.jwt_access_token_minutes,
    refresh_token_days=settings.jwt_refresh_token_days,
    secure=settings.jwt_cookie_secure,
    samesite=settings.jwt_cookie_samesite,
    domain=settings.jwt_cookie_domain,
)
