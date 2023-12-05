import hashlib
import random
from pathlib import Path

import filetype

from ..log import logger
from ..pp import only_file
from .consts import CHAR_SET, NAME_LENGTH


def rename_random(path: Path):
    """use random generator"""

    def rng():
        """random name generator"""
        char_list = random.choices(CHAR_SET, k=NAME_LENGTH)
        return ''.join(char_list)

    while True:
        new_path = path.with_stem(rng())  # v3.9+
        if not new_path.exists():
            break

    path.rename(new_path)
    logger.info(f'done: {path} --> {new_path}')


@only_file
def rename_extension(path: Path):
    """use filetype to determine extension"""
    content = path.read_bytes()
    ext = filetype.guess_extension(content)

    if ext is None:
        logger.error(f'cannot guess extension: {path.name}')
        return

    new_path = path.with_suffix(f'.{ext}')
    if new_path == path:
        logger.warning(f'exists: {new_path}')
    else:
        path.rename(new_path)
        logger.info(f'done: {path} --> {new_path}')


@only_file
def rename_md5(path: Path):
    """use file md5"""
    content = path.read_bytes()
    md5 = hashlib.md5(content)

    new_path = path.parent / (md5.hexdigest() + path.suffix)

    if new_path == path or new_path.exists():
        logger.warning(f'exists: {path} --> {new_path}')
    else:
        path.rename(new_path)
        logger.info(f'done: {path} --> {new_path}')


def rename_lower(path: Path):
    """convert to lower"""
    new_path = path.rename(path.with_name(path.name.lower()))

    logger.info(f'done: {path} --> {new_path}')


def rename_upper(path: Path):
    """convert to upper"""
    new_path = path.rename(path.with_name(path.name.upper()))

    logger.info(f'done: {path} --> {new_path}')
