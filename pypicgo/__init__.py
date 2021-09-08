import os
from pathlib import Path

home = os.path.expanduser('~')
HOME = Path(home)
BASE_DIR = HOME.joinpath('.PyPicGo')
if not BASE_DIR.exists():
    BASE_DIR.mkdir(parents=True)

__all__ = ["BASE_DIR"]

