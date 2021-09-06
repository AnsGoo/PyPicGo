from typing import Dict, Optional
from pypicgo.core.base.file import UploadFile


class Result:
    _status: bool
    _file: UploadFile
    _message: str
    origin_resp: Dict

    def __init__(self, status: bool,
                 file: UploadFile,
                 message: str,
                 remote_url:str = None,
                 origin_resp: Dict = dict()
                 ):
        self._status = status
        self._file = file
        self._message = message
        self.remote_url = remote_url
        self.origin_resp = origin_resp

    @property
    def status(self) -> bool:
        return self._status

    @status.setter
    def status(self, status: bool):
        if isinstance(status, bool):
            self._status = status
        else:
            raise ValueError('status must be bool')

    @property
    def file(self) -> UploadFile:
        return self._file

    @file.setter
    def file(self, file: UploadFile):
        if isinstance(file, UploadFile):
            self._file = file
        else:
            raise ValueError('file must be UploadFile')

    @property
    def message(self) -> str:
        return self._message

    @message.setter
    def message(self, message: str):
        if isinstance(message, str):
            self._message = message
        else:
            raise ValueError('message must be str')
