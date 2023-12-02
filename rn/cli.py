from typing import Optional

import click

from .job import (
    rename_extension,
    rename_lower,
    rename_md5,
    rename_add_prefix,
    rename_random,
    rename_remove_prefix,
    rename_upper,
    rename_add_suffix,
    rename_remove_suffix,
)
from .log import logger
from .pp import preprocess_0, preprocess_1
from .types import T_JOB_N


# https://github.com/pallets/click/issues/513#issuecomment-504158316
# https://zhuanlan.zhihu.com/p/73426505
# requires v3.6+
class OrderedGroup(click.Group):
    def list_commands(self, _) -> list[str]:
        return list(self.commands.keys())


@click.group(cls=OrderedGroup)
@click.option(
    '-f', '--only-file', type=bool, is_flag=True, default=False, help='only file'
)
@click.option(
    '-d', '--only-dir', type=bool, is_flag=True, default=False, help='only directory'
)
@click.pass_context
def cli(ctx: click.Context, only_file: bool, only_dir: bool):
    """rename file or directory with given condition"""
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


@cli.group(name='prefix', cls=OrderedGroup)
@click.pass_context
def cli_prefix(ctx: click.Context):
    """rename with prefix"""


@cli_prefix.command(name='add', help=rename_add_prefix.__doc__)
@click.pass_context
@click.argument('file', nargs=-1, required=True, type=str)
@click.option('--xfix', type=str, help='prefix')
@preprocess_1(rename_add_prefix)
def add_prefix(ctx: click.Context, file, xfix: Optional[str]):
    logger.debug(f'{ctx.obj=}')
    logger.debug(f'{file=}')
    logger.debug(f'{xfix=}')


@cli_prefix.command(name='rm', help=rename_remove_prefix.__doc__)
@click.pass_context
@click.argument('file', nargs=-1, required=True, type=str)
@click.option('--xfix', type=str, help='prefix')
@preprocess_1(rename_remove_prefix)
def remove_prefix(ctx: click.Context, file, xfix: Optional[str]):
    logger.debug(f'{ctx.obj=}')
    logger.debug(f'{file=}')
    logger.debug(f'{xfix=}')


@cli.group(name='suffix', cls=OrderedGroup)
@click.pass_context
def cli_suffix(ctx: click.Context):
    """rename with suffix"""


@cli_suffix.command(name='add', help=rename_add_suffix.__doc__)
@click.pass_context
@click.argument('file', nargs=-1, required=True, type=str)
@click.option('--xfix', type=str, help='suffix')
@preprocess_1(rename_add_suffix)
def add_suffix(ctx: click.Context, file, xfix: Optional[str]):
    logger.debug(f'{ctx.obj=}')
    logger.debug(f'{file=}')
    logger.debug(f'{xfix=}')


@cli_suffix.command(name='rm', help=rename_remove_suffix.__doc__)
@click.pass_context
@click.argument('file', nargs=-1, required=True, type=str)
@click.option('--xfix', type=str, help='suffix')
@preprocess_1(rename_remove_suffix)
def remove_suffix(ctx: click.Context, file, xfix: Optional[str]):
    logger.debug(f'{ctx.obj=}')
    logger.debug(f'{file=}')
    logger.debug(f'{xfix=}')
