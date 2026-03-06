from __future__ import annotations

from abc import ABC, abstractmethod


class StorageProvider(ABC):
    @abstractmethod
    def save(self, path: str, content: bytes) -> str:
        raise NotImplementedError

    @abstractmethod
    def delete(self, path: str) -> None:
        raise NotImplementedError
