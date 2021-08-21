from typing import ClassVar, Dict, List
from pypicgo.core.base.uploader import CommonUploader
from pypicgo.core.logger import logger
from pypicgo.core.exceptions import UploaderTypeException
from pypicgo.core.models import PluginModel


class create_uploader:

    def __init__(self, uploader_class: ClassVar[CommonUploader], config: Dict, plugins: List[PluginModel]):
        if issubclass(uploader_class, CommonUploader):
            self.uploader = uploader_class(plugins=plugins, **config)
            logger.info('create uploader successfully')
        else:
            raise UploaderTypeException()

    def __enter__(self):
        self.uploader.get_plugins()
        return self.uploader

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.uploader.final()
