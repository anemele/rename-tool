from pathlib import Path

from ..log import logger
from ..pp import if_exist_then_rename


@if_exist_then_rename
def rename_remove_prefix(path: Path, prefix: str) -> Path | None:
    """remove prefix, if `path` not starts with `prefix` then skip"""
    name = path.name

    if not name.startswith(prefix):
        logger.warning(f'not start with `{prefix}`: {path}')
        return

    return path.with_name(name.lstrip(prefix))


@if_exist_then_rename
def rename_add_prefix(path: Path, prefix: str):
    """prepend prefix"""
    return path.with_name(f'{prefix}{path.name}')


@if_exist_then_rename
def rename_remove_suffix(path: Path, suffix: str) -> Path | None:
    """remove suffix, if `path` not ends with `suffix` then skip"""
    name = path.stem

    if not name.endswith(suffix):
        logger.warning(f'not end with `{suffix}`: {path}')
        return

    return path.with_name(name.rstrip(suffix))


@if_exist_then_rename
def rename_add_suffix(path: Path, suffix: str):
    """prepend suffix"""
    return path.with_stem(f'{path.stem}{suffix}')
