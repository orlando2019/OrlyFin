from __future__ import annotations

from abc import ABC, abstractmethod


# Modela la responsabilidad de 'unit of work' dentro del dominio o capa actual.
class UnitOfWork(ABC):
    # Ejecuta la lógica principal de 'commit' y devuelve el resultado esperado por el flujo.
    @abstractmethod
    def commit(self) -> None:
        raise NotImplementedError

    # Ejecuta la lógica principal de 'rollback' y devuelve el resultado esperado por el flujo.
    @abstractmethod
    def rollback(self) -> None:
        raise NotImplementedError
