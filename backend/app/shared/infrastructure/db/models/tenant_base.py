from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column


# Modela la responsabilidad de 'tenant base mixin' dentro del dominio o capa actual.
class TenantBaseMixin:
    organization_id: Mapped[str] = mapped_column(String(36), index=True)
