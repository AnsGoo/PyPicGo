import hashlib
import datetime
from pathlib import Path
from core.base.plugin import BeforePlugin
from core.base.file import UploadFile


class ReNamePlugin(BeforePlugin):
    name = 'MD5 ReName'

    def execute(self, file:UploadFile) -> UploadFile:
        filename = file.filename
        myhash = hashlib.md5()
        now = datetime.datetime.now().strftime("%Y%m%d%H%M%S")
        f = open(file.tempfile.resolve(), 'rb')
        while True:
            b = f.read(8096)
            if not b:
                break
            myhash.update(b)
        f.close()
        md5 = myhash.hexdigest()
        file.filename = f'{md5}-{now}-{filename}'
        return file
