import os
from typing import List, Any

from pypicgo.core.base.plugin import BeforePlugin, AfterPlugin, FinallyPlugin
from pypicgo.core.models import PluginModel
from pypicgo.core.utils.modules import import_string
from pypicgo.core.exceptions import (NotImplementedException, PluginExecuteException)
from pypicgo.core.logger import logger
from pypicgo.core.base.file import UploadFile
from pypicgo.core.base.result import Result


class BaseUploader:
    name = 'base_uploader'


class CommonUploader(BaseUploader):
    type = 'uploader'
    _plugins: List[PluginModel] = []
    _after_plugins: List[Any] = []
    _before_plugins: List[Any] = []
    _final_plugins: List[Any] = []
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

    def upload(self) -> Result:
        raise NotImplementedException()

    def load_config(self, **kwargs):
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
                logger.warning(f'loader {plugin.module} plugins failed,please check the plugin config')
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
                plugin.execute(result)
                logger.info(f'plugins [{plugin.name}] execute successfully')
            except PluginExecuteException as e:
                logger.warning(f'plugins [{plugin.name}] execute fail')

    def execute_final_plugins(self, results: List[Result]):
        for plugin in self._final_plugins:
            try:
                plugin.execute(results)
                logger.info(f'plugins [{plugin.name}] execute successfully')
            except PluginExecuteException as e:
                logger.warning(f'plugins [{plugin.name}] execute fail')

    def do(self, filepath):
        file = UploadFile(filepath)
        self.file = file
        self.execute_before_plugins()
        self.result = self.upload()
        if isinstance(self.result, Result):
            self.results.append(self.result)
            if self.result.status is not None:
                self.execute_after_plugins(self.result)
            if not self.file.origin_file.resolve() == self.file.tempfile.resolve():
                os.remove(self.file.tempfile.resolve())
        else:
            logger.warn(f'upload method of [{self.name}] uploader must return a Result object')
            raise Exception(f'upload method of [{self.name}] uploader must return a Result object')

    def final(self):
        self.execute_final_plugins(self.results)
