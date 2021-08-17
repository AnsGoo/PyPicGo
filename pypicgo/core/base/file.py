from pathlib import Path
from pypicgo.core.exceptions import (PathNotExistsException, IsNotFileException)
from pypicgo.core.logger import logger


class UploadFile:

    def __init__(self, filepath):
        file = Path(filepath)
        if not file.exists():
            raise PathNotExistsException()
        if not file.is_file():
            raise IsNotFileException()
        self.origin_file = file
        self.filename = file.name
        self._tempfile = file
        logger.info('uploadfile create successfully')

    @property
    def tempfile(self):
        return self._tempfile

    @tempfile.setter
    def tempfile(self, file: Path):
        if isinstance(file, Path):
            if not file.exists():
                raise PathNotExistsException()
            if not file.is_file():
                raise IsNotFileException()
            self._tempfile = file

    def __str__(self):
        return self._tempfile.resolve()
