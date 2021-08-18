import os
import platform
from pathlib import Path

system_name = platform.system().lower()

if system_name == 'linux':
    HOME = os.environ.get('HOME')
    home = Path(HOME)
elif system_name == 'windows':
    HOMEDRIVE = os.environ.get('HOMEDRIVE')
    HOME = os.environ.get('HOMEPATH')
    home = Path(HOMEDRIVE).joinpath(HOME)
BASE_DIR = home.joinpath('.PyPicGO')
if not BASE_DIR.exists():
    BASE_DIR.mkdir(parents=True)

__all__ = ["BASE_DIR"]

