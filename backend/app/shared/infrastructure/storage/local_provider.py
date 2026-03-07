from __future__ import annotations

from pathlib import Path

from app.shared.infrastructure.storage.interface import StorageProvider


class LocalStorageProvider(StorageProvider):
    def __init__(self, base_path: str = "./storage") -> None:
        self.base_path = Path(base_path).resolve()
        self.base_path.mkdir(parents=True, exist_ok=True)

    def _safe_target(self, path: str) -> Path:
        target = (self.base_path / path).resolve()
        try:
            target.relative_to(self.base_path)
        except ValueError as exc:
            raise ValueError("Unsafe storage path outside base directory") from exc
        return target

    def save(self, path: str, content: bytes) -> str:
        target = self._safe_target(path)
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_bytes(content)
        return str(target)

    def delete(self, path: str) -> None:
        target = self._safe_target(path)
        if target.exists():
            target.unlink()
