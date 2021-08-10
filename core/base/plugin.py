from pathlib import Path
from requests import Response
from typing import List
from core.base.result import Result
from core.exceptions import NotImplementedException



class BasePlugin:
    name = 'base_plugin'

    def __init__(self, **kwargs):
        pass


class BeforePlugin(BasePlugin):
    type = 'before'

    def execute(self, file: Path) -> Path:
        raise NotImplementedException()


class AfterPlugin(BasePlugin):
    type = 'after'

    def execute(self, result: Result):
        raise NotImplementedException()


class FinallyPlugin(BasePlugin):
    type = 'final'

    def execute(self, results: List[Result]):
        raise NotImplementedException()
