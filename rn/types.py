from pathlib import Path
from typing import Callable, Optional

T_JOB_N = Callable[[Path], None]
T_JOB_P = Callable[[Path, str], Optional[Path]]
T_JOB = Callable
