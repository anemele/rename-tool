from pathlib import Path
from typing import Optional

from ..log import logger
from ..pp import if_exist_then_rename


@if_exist_then_rename
def rename_remove_prefix(filepath: Path, prefix: str) -> Optional[Path]:
    """remove prefix, if `filepath` not starts with `prefix` then skip"""
    name = filepath.name

    if not name.startswith(prefix):
        logger.warning(f'not start with `{prefix}`: {filepath}')
        return

    return filepath.with_name(name.lstrip(prefix))


@if_exist_then_rename
def rename_prepend_prefix(filepath: Path, prefix: str):
    """prepend prefix"""
    return filepath.with_name(f'{prefix}{filepath.name}')
