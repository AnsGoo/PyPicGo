# from pydantic import BaseModel
from typing import Dict, Optional, List


class PluginModel:
    module: str
    config: Optional[Dict] = None

    def __init__(self,module:str, config:Optional[Dict] = None) -> None:
       self.module = module
       self.config = config


class UploaderModel:
    module: str
    config: Optional[Dict] = None
    def __init__(self,module:str, config:Optional[Dict] = None) -> None:
       self.module = module
       self.config = config


class ConfigModel:
    uploader: UploaderModel
    plugins: List[PluginModel]

    def __init__(self,uploader:UploaderModel, plugins:List[PluginModel]) -> None:
       self.uploader = uploader
       self.plugins = plugins
