import sys

from .cli import cli

# read the source
# at `click/core.py:BaseCommand:main`
cli(args=sys.argv[2:], prog_name=sys.argv[1])
