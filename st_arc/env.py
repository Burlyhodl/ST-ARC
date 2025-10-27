"""Environment loading utilities for ST-ARC tools."""

from __future__ import annotations

import os
from pathlib import Path
from typing import Iterable

PROJECT_ROOT = Path(__file__).resolve().parents[1]
DEFAULT_ENV_PATH = PROJECT_ROOT / ".env"
ENV_FILE_ENV_VAR = "ST_ARC_ENV_FILE"


def load_env(
    env_file: str | os.PathLike[str] | None = None,
    *,
    overwrite: bool = False,
) -> Path | None:
    """Load key=value pairs from a .env-style file into ``os.environ``.

    The loader keeps any variables that are already defined in the environment and only
    fills in missing values. Lines beginning with ``#`` are ignored, as are blank lines.
    Values wrapped in single or double quotes are unwrapped.

    Args:
        env_file: Optional override for the .env path. When omitted the function checks
            the ``ST_ARC_ENV_FILE`` environment variable and then ``PROJECT_ROOT/.env``.
        overwrite: When ``True``, values from the env file replace existing entries in
            ``os.environ``. By default, existing values are preserved.

    Returns:
        The path to the environment file that was loaded, or ``None`` if no file was
        found.
    """

    candidate = _resolve_env_path(env_file)
    if candidate is None:
        return None

    was_explicit = env_file is not None or os.getenv(ENV_FILE_ENV_VAR)
    if not candidate.exists():
        if was_explicit:
            raise FileNotFoundError(f"Environment file '{candidate}' does not exist.")
        return None

    for key, value in _parse_env_file(candidate):
        if overwrite or key not in os.environ:
            os.environ[key] = value
    return candidate


def _resolve_env_path(env_file: str | os.PathLike[str] | None) -> Path | None:
    if env_file is not None:
        return Path(env_file)

    env_override = os.getenv(ENV_FILE_ENV_VAR)
    if env_override:
        return Path(env_override)

    return DEFAULT_ENV_PATH


def _parse_env_file(path: Path) -> Iterable[tuple[str, str]]:
    try:
        lines = path.read_text(encoding="utf-8").splitlines()
    except OSError as exc:  # noqa: PLE0704
        raise RuntimeError(f"Failed to read environment file '{path}': {exc}") from exc

    for raw_line in lines:
        line = raw_line.strip()
        if not line or line.startswith("#"):
            continue

        if line.lower().startswith("export "):
            line = line[7:]

        if "=" not in line:
            continue

        key, value = line.split("=", 1)
        key = key.strip()
        value = _strip_quotes(value.strip())

        if key:
            yield key, value


def _strip_quotes(value: str) -> str:
    if len(value) >= 2 and value[0] == value[-1] and value[0] in {'"', "'"}:
        return value[1:-1]
    return value


__all__ = ["load_env"]
