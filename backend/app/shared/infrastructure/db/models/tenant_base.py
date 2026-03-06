from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column


class TenantBaseMixin:
    organization_id: Mapped[str] = mapped_column(String(36), index=True)
