from __future__ import annotations

from pathlib import Path

import pytest

from app.shared.infrastructure.storage.local_provider import LocalStorageProvider


def test_local_storage_rejects_path_traversal(tmp_path: Path) -> None:
    storage = LocalStorageProvider(base_path=str(tmp_path / "attachments"))

    with pytest.raises(ValueError):
        storage.save("../outside.txt", b"nope")


def test_local_storage_accepts_safe_relative_path(tmp_path: Path) -> None:
    storage = LocalStorageProvider(base_path=str(tmp_path / "attachments"))
    saved_path = storage.save("org/module/entity/file.txt", b"ok")

    assert Path(saved_path).exists()
