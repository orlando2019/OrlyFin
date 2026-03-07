from pydantic import BaseModel


# Modela la responsabilidad de 'health response' dentro del dominio o capa actual.
class HealthResponse(BaseModel):
    status: str
    service: str
    version: str
    timestamp: str
