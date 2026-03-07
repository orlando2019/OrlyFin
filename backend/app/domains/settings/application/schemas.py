from __future__ import annotations

from typing import Any

from pydantic import BaseModel, Field


class SettingUpsertRequest(BaseModel):
    key: str = Field(min_length=2, max_length=120)
    value: Any
    value_type: str = Field(default="string")
    is_sensitive: bool = False


class SettingResponse(BaseModel):
    key: str
    value: Any
    value_type: str
    is_sensitive: bool


class SettingListResponse(BaseModel):
    settings: list[SettingResponse]
