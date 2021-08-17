from pypicgo.core.base.file import UploadFile
from requests import Response


class Result:
    _status: bool
    _resp: Response
    _file: UploadFile
    _message: str

    def __init__(self, status: bool,
                 resp: Response,
                 file: UploadFile,
                 message: str):
        self.status = status
        self.resp = resp
        self.file = file
        self.message = message

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
    def resp(self) -> Response:
        return self._resp

    @resp.setter
    def resp(self, resp: Response):
        if isinstance(resp, Response):
            self._resp = resp
        else:
            raise ValueError('resp must be response')

    @property
    def message(self) -> str:
        return self._message

    @message.setter
    def message(self, message: str):
        if isinstance(message, str):
            self._message = message
        else:
            raise ValueError('message must be str')
