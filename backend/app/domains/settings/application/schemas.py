from __future__ import annotations

from typing import Any

from pydantic import BaseModel, Field


# Modela la responsabilidad de 'setting upsert request' dentro del dominio o capa actual.
class SettingUpsertRequest(BaseModel):
    key: str = Field(min_length=2, max_length=120)
    value: Any
    value_type: str = Field(default="string")
    is_sensitive: bool = False


# Modela la responsabilidad de 'setting response' dentro del dominio o capa actual.
class SettingResponse(BaseModel):
    key: str
    value: Any
    value_type: str
    is_sensitive: bool


# Modela la responsabilidad de 'setting list response' dentro del dominio o capa actual.
class SettingListResponse(BaseModel):
    settings: list[SettingResponse]
