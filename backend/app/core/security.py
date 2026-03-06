from __future__ import annotations

import base64
import hashlib
import hmac
import os
from dataclasses import dataclass
from datetime import datetime, timedelta, timezone
from typing import Any

import jwt

from app.core.config import Settings, settings


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


def hash_password(plain_password: str) -> str:
    iterations = 210_000
    salt = os.urandom(16)
    digest = hashlib.pbkdf2_hmac("sha256", plain_password.encode("utf-8"), salt, iterations)
    salt_b64 = base64.b64encode(salt).decode("utf-8")
    digest_b64 = base64.b64encode(digest).decode("utf-8")
    return f"pbkdf2_sha256${iterations}${salt_b64}${digest_b64}"


def verify_password(plain_password: str, hashed_password: str) -> bool:
    try:
        algorithm, iterations_str, salt_b64, digest_b64 = hashed_password.split("$", 3)
        if algorithm != "pbkdf2_sha256":
            return False
        iterations = int(iterations_str)
        salt = base64.b64decode(salt_b64.encode("utf-8"))
        expected_digest = base64.b64decode(digest_b64.encode("utf-8"))
    except (ValueError, TypeError):
        return False

    candidate_digest = hashlib.pbkdf2_hmac("sha256", plain_password.encode("utf-8"), salt, iterations)
    return hmac.compare_digest(candidate_digest, expected_digest)


def _build_token_payload(subject: str, token_type: str, expires_delta: timedelta, claims: dict[str, Any] | None = None) -> dict[str, Any]:
    now = datetime.now(timezone.utc)
    payload: dict[str, Any] = {
        "sub": subject,
        "type": token_type,
        "iat": int(now.timestamp()),
        "exp": int((now + expires_delta).timestamp()),
    }
    if claims:
        payload.update(claims)
    return payload


def create_access_token(subject: str, claims: dict[str, Any] | None = None, config: Settings = settings) -> str:
    payload = _build_token_payload(
        subject=subject,
        token_type="access",
        expires_delta=timedelta(minutes=config.jwt_access_token_minutes),
        claims=claims,
    )
    return jwt.encode(payload, config.jwt_access_secret_key, algorithm=config.jwt_algorithm)


def create_refresh_token(subject: str, claims: dict[str, Any] | None = None, config: Settings = settings) -> str:
    payload = _build_token_payload(
        subject=subject,
        token_type="refresh",
        expires_delta=timedelta(days=config.jwt_refresh_token_days),
        claims=claims,
    )
    return jwt.encode(payload, config.jwt_refresh_secret_key, algorithm=config.jwt_algorithm)


def decode_access_token(token: str, config: Settings = settings) -> dict[str, Any]:
    return jwt.decode(token, config.jwt_access_secret_key, algorithms=[config.jwt_algorithm])


def decode_refresh_token(token: str, config: Settings = settings) -> dict[str, Any]:
    return jwt.decode(token, config.jwt_refresh_secret_key, algorithms=[config.jwt_algorithm])
