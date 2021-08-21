from typing import List
from pypicgo.core.base.result import Result
from pypicgo.core.base.file import UploadFile
from pypicgo.core.exceptions import NotImplementedException


class BasePlugin:
    name = 'base_plugin'

    def __init__(self, **kwargs):
        pass


class BeforePlugin(BasePlugin):
    type = 'before'

    def execute(self, file: UploadFile) -> UploadFile:
        raise NotImplementedException()


class AfterPlugin(BasePlugin):
    type = 'after'

    def execute(self, result: Result):
        raise NotImplementedException()


class FinallyPlugin(BasePlugin):
    type = 'final'

    def execute(self, results: List[Result]):
        raise NotImplementedException()
