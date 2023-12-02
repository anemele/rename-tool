import hashlib
import random
from pathlib import Path

import filetype

from ..log import logger
from ..pp import only_file
from .consts import CHAR_SET, NAME_LENGTH


def rename_random(filepath: Path):
    """use random generator"""

    def rng():
        """random name generator"""
        char_list = random.choices(CHAR_SET, k=NAME_LENGTH)
        return ''.join(char_list)

    while True:
        new_path = filepath.with_stem(rng())  # v3.9+
        if not new_path.exists():
            break

    filepath.rename(new_path)
    logger.info(f'done: {filepath} --> {new_path}')


@only_file
def rename_extension(filepath: Path):
    """use filetype to determine extension"""
    content = filepath.read_bytes()
    ext = filetype.guess_extension(content)

    if ext is None:
        logger.error(f'cannot guess extension: {filepath.name}')
        return

    new_path = filepath.with_suffix(f'.{ext}')
    if new_path == filepath:
        logger.warning(f'exists: {new_path}')
    else:
        filepath.rename(new_path)
        logger.info(f'done: {filepath} --> {new_path}')


@only_file
def rename_md5(filepath: Path):
    """use file md5"""
    content = filepath.read_bytes()
    md5 = hashlib.md5(content)

    new_path = filepath.parent / (md5.hexdigest() + filepath.suffix)

    if new_path == filepath or new_path.exists():
        logger.warning(f'exists: {filepath} --> {new_path}')
    else:
        filepath.rename(new_path)
        logger.info(f'done: {filepath} --> {new_path}')


def rename_lower(filepath: Path):
    """convert to lower"""
    new_path = filepath.rename(filepath.with_name(filepath.name.lower()))

    logger.info(f'done: {filepath} --> {new_path}')


def rename_upper(filepath: Path):
    """convert to upper"""
    new_path = filepath.rename(filepath.with_name(filepath.name.upper()))

    logger.info(f'done: {filepath} --> {new_path}')
