import os
from requests import Response
from typing import List, Any

from core.base.plugin import BeforePlugin, AfterPlugin, FinallyPlugin
from core.models import PluginModel
from core.utils.modules import import_string
from core.exceptions import (NotImplementedException, PluginExecuteException)
from core.logger import logger
from core.base.file import UploadFile
from core.base.result import Result


class BaseUploader:
    name = 'base_uploader'


class CommonUploader(BaseUploader):
    type = 'uploader'
    _plugins: List[PluginModel] = []
    _after_plugins: List[Any] = []
    _before_plugins: List[Any] = []
    _final_plugins: List[Any] = []
    resp = None
    file = None
    result = None
    results: List[Result] = []

    @property
    def plugins(self):
        return self._plugins

    @plugins.setter
    def plugins(self, plugins: List[PluginModel]):
        if plugins:
            self._plugins = plugins
        else:
            self._plugins = []

    def __init__(self, plugins: List[PluginModel], **kwargs):
        self.plugins = plugins
        self.load_config(**kwargs)

    def upload(self) -> Response:
        raise NotImplementedException()

    def load_config(self, **kwargs):
        raise NotImplementedException()

    def is_success(self, resp: Response):
        raise NotImplementedException()

    def get_plugins(self):
        self._after_plugins = []
        self._before_plugins = []
        self._final_plugins = []
        for plugin in self.plugins:
            try:
                module = import_string(plugin.module)
                config = plugin.config if plugin.config else dict()
                if issubclass(module, BeforePlugin):
                    self._before_plugins.append(module(**config))
                elif issubclass(module, AfterPlugin):
                    self._after_plugins.append(module(**config))
                elif issubclass(module, FinallyPlugin):
                    self._final_plugins.append((module(**config)))
            except ImportError:
                continue
        logger.info('loader plugins successfully')

    def execute_before_plugins(self) -> UploadFile:
        for plugin in self._before_plugins:
            try:
                self.file = plugin.execute(self.file)
                logger.info(f'plugins [{plugin.name}] execute successfully')
            except PluginExecuteException as e:
                logger.warning(f'plugins [{plugin.name}] execute fail')

        return self.file

    def execute_after_plugins(self, result: Result):
        for plugin in self._after_plugins:
            try:
                self.resp = plugin.execute(result)
                logger.info(f'plugins [{plugin.name}] execute successfully')
            except PluginExecuteException as e:
                logger.warning(f'plugins [{plugin.name}] execute fail')

    def execute_final_plugins(self, results: List[Result]):
        for plugin in self._final_plugins:
            try:
                self.resp = plugin.execute(results)
                logger.info(f'plugins [{plugin.name}] execute successfully')
            except PluginExecuteException as e:
                logger.warning(f'plugins [{plugin.name}] execute fail')

    def do(self, filepath):
        file = UploadFile(filepath)
        self.file = file
        self.execute_before_plugins()
        resp = self.upload()
        status, message = self.is_success(resp)
        result = Result(status=status, resp=resp, file=file, message=message)
        self.result = result
        self.results.append(result)
        if isinstance(self.result.resp, Response):
            self.execute_after_plugins(result)

    def final(self):
        if isinstance(self.result.resp, Response):
            self.execute_final_plugins(self.results)
            if not self.file.origin_file.resolve() == self.file.tempfile.resolve():
                os.remove(self.file.tempfile.resolve())
