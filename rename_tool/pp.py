import glob
from functools import wraps
from itertools import chain
from os.path import isdir, isfile
from pathlib import Path
from typing import Tuple

import click

from .log import logger
from .types import T_JOB, T_JOB_P


def preprocess_0(job: T_JOB):
    def decorator(func):
        @wraps(func)
        def wrapper(ctx: click.Context, file: Tuple[str]):
            logger.debug(f'{ctx.obj=}')
            logger.debug(f'{file=}')

            file_list = chain.from_iterable(map(glob.iglob, file))
            if ctx.obj['f']:
                file_list = filter(isfile, file_list)
            if ctx.obj['d']:
                file_list = filter(isdir, file_list)

            for path in map(Path, file_list):
                job(path)

        return wrapper

    return decorator


def preprocess_1(job: T_JOB_P):
    def decorator(func):
        @wraps(func)
        def wrapper(ctx: click.Context, file: Tuple[str], xfix: str | None):
            logger.debug(f'{ctx.obj=}')
            logger.debug(f'{file=}')
            logger.debug(f'{xfix=}')

            if xfix is None:
                logger.error('no pre/suf-fix given')
                return

            file_list = chain.from_iterable(map(glob.iglob, file))
            if ctx.obj['f']:
                file_list = filter(isfile, file_list)
            if ctx.obj['d']:
                file_list = filter(isdir, file_list)

            for path in map(Path, file_list):
                job(path, xfix)

        return wrapper

    return decorator
