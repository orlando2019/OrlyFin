from __future__ import annotations

from fastapi import Request


def get_trace_id(request: Request) -> str:
    return getattr(request.state, "trace_id", "")
