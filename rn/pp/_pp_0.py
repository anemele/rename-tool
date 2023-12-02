import glob
from functools import wraps
from itertools import chain
from os.path import isdir, isfile
from pathlib import Path
from typing import Tuple

import click

from ..log import logger
from ..types import T_JOB, T_JOB_N


def only_file(func: T_JOB_N):
    @wraps(func)
    def wrapper(file: Path):
        if not file.is_file():
            logger.error(f'not a file: {file}')
            return

        return func(file)

    return wrapper


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

            return func(ctx, file)

        return wrapper

    return decorator
