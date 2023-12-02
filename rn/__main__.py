from .cli import cli

if __name__ == '__main__':
    # read the source
    # at `click/core.py:BaseCommand:main`
    cli(prog_name=__package__)
