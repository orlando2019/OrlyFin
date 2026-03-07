from __future__ import annotations

from abc import ABC, abstractmethod


# Modela la responsabilidad de 'storage provider' dentro del dominio o capa actual.
class StorageProvider(ABC):
    # Ejecuta la lógica principal de 'save' y devuelve el resultado esperado por el flujo.
    @abstractmethod
    def save(self, path: str, content: bytes) -> str:
        raise NotImplementedError

    # Ejecuta la lógica principal de 'delete' y devuelve el resultado esperado por el flujo.
    @abstractmethod
    def delete(self, path: str) -> None:
        raise NotImplementedError
