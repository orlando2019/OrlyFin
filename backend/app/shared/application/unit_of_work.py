from __future__ import annotations

from abc import ABC, abstractmethod


class UnitOfWork(ABC):
    @abstractmethod
    def commit(self) -> None:
        raise NotImplementedError

    @abstractmethod
    def rollback(self) -> None:
        raise NotImplementedError
