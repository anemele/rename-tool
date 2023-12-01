import hashlib
import random
import string
from pathlib import Path

import filetype

from .log import logger

CHAR_SET = string.ascii_lowercase + string.digits
NAME_LENGTH = 6


def rename_random(filepath: str):
    """use random generator"""
    path = Path(filepath)
    suffix = path.suffix

    while True:
        char_list = random.choices(CHAR_SET, k=NAME_LENGTH)
        name = ''.join(char_list)
        new_name = Path(f'{name}{suffix}')
        if new_name.exists():
            continue
        path.rename(new_name)

        logger.info(f'done: {filepath} --> {new_name}')
        break


def rename_extension(filepath: str):
    """use filetype to determine extension"""
    path = Path(filepath)
    if not path.is_file():
        logger.error(f'not a file: {filepath}')
        return

    content = path.read_bytes()
    ext = filetype.guess_extension(content)

    if ext is None:
        logger.error(f'cannot guess extension: {path.name}')
        return

    new_name = path.with_suffix(f'.{ext}')
    if new_name == filepath:
        logger.warning(f'exists: {new_name}')
    else:
        path.rename(new_name)
        logger.info(f'done: {filepath} --> {new_name}')


def rename_md5(filepath: str):
    """use file md5"""
    path = Path(filepath)
    if not path.is_file():
        logger.error(f'not a file: {filepath}')
        return

    content = path.read_bytes()
    md5 = hashlib.md5(content)

    new_path = path.parent / (md5.hexdigest() + path.suffix)

    if new_path == filepath or new_path.exists():
        logger.warning(f'exists: {filepath} --> {new_path}')
    else:
        path.rename(new_path)
        logger.info(f'done: {filepath} --> {new_path}')


def rename_lower(filepath: str):
    """convert to lower"""
    path = Path(filepath)
    new = path.rename(path.with_name(path.name.lower()))

    logger.info(f'done: {path} --> {new}')


def rename_upper(filepath: str):
    """convert to upper"""
    path = Path(filepath)
    new = path.rename(path.with_name(path.name.upper()))

    logger.info(f'done: {path} --> {new}')
