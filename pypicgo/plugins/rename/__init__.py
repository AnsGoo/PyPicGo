import datetime
import hashlib
import re

from pypicgo.core.base.file import UploadFile
from pypicgo.core.base.plugin import BeforePlugin


class ReNamePlugin(BeforePlugin):
    name = 'ReName'

    def __init__(self, format=None):
        self.format = format
        super().__init__()

    def execute(self, file: UploadFile) -> UploadFile:
        suffix = file.tempfile.suffix
        if not self.format:
            return file
        else:
            names = self.parse(self.format)
            func_map = self.get_variable_func()
            for index in range(len(names)):
                name = names[index]
                if name in func_map:
                    names[index] = func_map[name](file)
            filename = ''.join(names)
            file.filename = f'{filename}{suffix}'
            return file

    def _date(self, file: UploadFile) -> str:
        return datetime.datetime.now().strftime("%Y%m%d%H%M%S")

    def _hash(self, file: UploadFile) -> str:
        myhash = hashlib.md5()
        f = open(file.tempfile.resolve(), 'rb')
        while True:
            b = f.read(8096)
            if not b:
                break
            myhash.update(b)
        f.close()
        md5 = myhash.hexdigest()
        return md5

    def _filename(self, file: UploadFile) -> str:
        return file.filename.split('.')[0]

    def _location(self, file: UploadFile) -> str:
        path = str(file.origin_file.resolve())
        filename = file.origin_file.name
        location = path.split(filename)[0]
        return location

    def get_variable_func(self):
        func_map = {
            'location': self._location,
            'filename': self._filename,
            'hash': self._hash,
            'date': self._date
        }
        return func_map

    def parse(self, format: str):
        # variables = re.findall(r'[{](.*?)[}]', format)
        names = re.split(r'[{}]', format)
        return names
