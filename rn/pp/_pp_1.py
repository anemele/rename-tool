import glob
from functools import wraps
from itertools import chain
from os.path import isdir, isfile
from pathlib import Path
from typing import Optional, Tuple

import click

from ..log import logger
from ..types import T_JOB_P


def if_exist_then_rename(func: T_JOB_P):
    @wraps(func)
    def wrapper(filepath: Path, prefix: str):
        new_path = func(filepath, prefix)
        if new_path is None:
            return

        if new_path.exists():
            logger.error(f'exists: {new_path}')
        else:
            filepath.rename(new_path)
            logger.info(f'done: {filepath} --> {new_path}')

    return wrapper


def preprocess_1(job: T_JOB_P):
    def decorator(func):
        @wraps(func)
        def wrapper(ctx: click.Context, file: Tuple[str], xfix: Optional[str]):
            logger.debug(f'{ctx.obj=}')
            logger.debug(f'{file=}')
            logger.debug(f'{xfix=}')

            file_list = chain.from_iterable(map(glob.iglob, file))
            if ctx.obj['f']:
                file_list = filter(isfile, file_list)
            if ctx.obj['d']:
                file_list = filter(isdir, file_list)

            xfix_ = '' if xfix is None else xfix
            for path in map(Path, file_list):
                job(path, xfix_)

            return func(ctx, file, xfix)

        return wrapper

    return decorator
