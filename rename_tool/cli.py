from typing import Optional

import click

from .core import (
    rename_add_prefix,
    rename_add_suffix,
    rename_extension,
    rename_lower,
    rename_md5,
    rename_random,
    rename_remove_prefix,
    rename_remove_suffix,
    rename_upper,
)
from .log import logger
from .pp import preprocess_0, preprocess_1


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


@cli.command(name='rand', help=rename_random.__doc__)
@click.pass_context
@click.argument('file', nargs=-1, required=True, type=str)
@preprocess_0(rename_random)
def cmd_random(ctx: click.Context, file):
    ...


@cli.command(name='ext', help=rename_extension.__doc__)
@click.pass_context
@click.argument('file', nargs=-1, required=True, type=str)
@preprocess_0(rename_extension)
def cmd_ext(ctx: click.Context, file):
    ...


@cli.command(name='md5', help=rename_md5.__doc__)
@click.pass_context
@click.argument('file', nargs=-1, required=True, type=str)
@preprocess_0(rename_md5)
def cmd_md5(ctx: click.Context, file):
    ...


@cli.command(name='low', help=rename_lower.__doc__)
@click.pass_context
@click.argument('file', nargs=-1, required=True, type=str)
@preprocess_0(rename_lower)
def cmd_low(ctx: click.Context, file):
    ...


@cli.command(name='upp', help=rename_upper.__doc__)
@click.pass_context
@click.argument('file', nargs=-1, required=True, type=str)
@preprocess_0(rename_upper)
def cmd_upp(ctx: click.Context, file):
    ...


@cli.group(name='prefix', cls=OrderedGroup)
@click.pass_context
def cli_prefix(ctx: click.Context):
    """rename with prefix"""


@cli_prefix.command(name='add', help=rename_add_prefix.__doc__)
@click.pass_context
@click.argument('file', nargs=-1, required=True, type=str)
@click.option('-f', '--xfix', type=str, help='prefix')
@preprocess_1(rename_add_prefix)
def cmd_add_prefix(ctx: click.Context, file, xfix: Optional[str]):
    ...


@cli_prefix.command(name='rm', help=rename_remove_prefix.__doc__)
@click.pass_context
@click.argument('file', nargs=-1, required=True, type=str)
@click.option('-f', '--xfix', type=str, help='prefix')
@preprocess_1(rename_remove_prefix)
def cmd_remove_prefix(ctx: click.Context, file, xfix: Optional[str]):
    ...


@cli.group(name='suffix', cls=OrderedGroup)
@click.pass_context
def cli_suffix(ctx: click.Context):
    """rename with suffix"""


@cli_suffix.command(name='add', help=rename_add_suffix.__doc__)
@click.pass_context
@click.argument('file', nargs=-1, required=True, type=str)
@click.option('-f', '--xfix', type=str, help='suffix')
@preprocess_1(rename_add_suffix)
def cmd_add_suffix(ctx: click.Context, file, xfix: Optional[str]):
    ...


@cli_suffix.command(name='rm', help=rename_remove_suffix.__doc__)
@click.pass_context
@click.argument('file', nargs=-1, required=True, type=str)
@click.option('-f', '--xfix', type=str, help='suffix')
@preprocess_1(rename_remove_suffix)
def cmd_remove_suffix(ctx: click.Context, file, xfix: Optional[str]):
    ...
