from __future__ import annotations

from fastapi import Request
from sqlalchemy.orm import Session

from app.shared.infrastructure.db.session import SessionLocal


def get_trace_id(request: Request) -> str:
    return getattr(request.state, "trace_id", "")


def get_db() -> Session:
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
