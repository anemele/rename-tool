from __future__ import annotations

import fire

from .jobs import *

if __name__ == '__main__':
    fire.Fire(
        dict(
            rand=rename_random,
            md5=rename_md5,
            upp=rename_upper,
            low=rename_lower,
            ext=rename_extension,
        ),
        name=__package__,
    )
