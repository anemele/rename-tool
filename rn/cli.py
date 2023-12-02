from typing import Optional
import click

from .job import (
    rename_extension,
    rename_lower,
    rename_md5,
    rename_prepend_prefix,
    rename_random,
    rename_remove_prefix,
    rename_upper,
)
from .log import logger
from .pp import preprocess_0, preprocess_1
from .types import T_JOB_N


@click.group(help='rename file or directory with given condition')
@click.option(
    '-f', '--only-file', type=bool, is_flag=True, default=False, help='only file'
)
@click.option(
    '-d', '--only-dir', type=bool, is_flag=True, default=False, help='only directory'
)
@click.pass_context
def cli(ctx: click.Context, only_file: bool, only_dir: bool):
    logger.debug(f'{only_file=}')
    logger.debug(f'{only_dir=}')
    ctx.obj = dict(f=only_file, d=only_dir)


def _gen(f: T_JOB_N, fn: str):
    exec(
        f'''
@cli.command(help='{f.__doc__}')
@click.pass_context
@click.argument('file', nargs=-1, required=True, type=str)
@{preprocess_0.__name__}({f.__name__})
def {fn}(ctx: click.Context, file):
    logger.debug(f'{{ctx.obj=}}')
    logger.debug(f'{{file=}}')
    '''
    )


_gen(rename_random, 'r')
_gen(rename_extension, 'ext')
_gen(rename_md5, 'md5')
_gen(rename_lower, 'low')
_gen(rename_upper, 'upp')


@cli.command(help=rename_prepend_prefix.__doc__)
@click.pass_context
@click.argument('file', nargs=-1, required=True, type=str)
@click.option('-p', '--prefix', type=str, help='prefix')
@preprocess_1(rename_prepend_prefix)
def add_prefix(ctx: click.Context, file, prefix: str):
    logger.debug(f'{ctx.obj=}')
    logger.debug(f'{file=}')
    logger.debug(f'{prefix=}')


@cli.command(help=rename_remove_prefix.__doc__)
@click.pass_context
@click.argument('file', nargs=-1, required=True, type=str)
@click.option('-p', '--prefix', type=str, help='prefix')
@preprocess_1(rename_remove_prefix)
def rm_prefix(ctx: click.Context, file, prefix: Optional[str]):
    logger.debug(f'{ctx.obj=}')
    logger.debug(f'{file=}')
    logger.debug(f'{prefix=}')
