import hashlib
import random
from functools import wraps
from pathlib import Path


from ..log import logger
from ..types import T_JOB_N
from .consts import CHAR_SET, NAME_LENGTH


def only_file(func: T_JOB_N):
    @wraps(func)
    def wrapper(file: Path):
        if not file.is_file():
            logger.error(f'not a file: {file}')
            return

        return func(file)

    return wrapper


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
