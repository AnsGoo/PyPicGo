from pydantic import BaseModel
from typing import Dict, Optional, List


class PluginModel(BaseModel):
    module: str
    config: Optional[Dict] = None


class UploaderModel(BaseModel):
    name: str
    module: str
    config: Optional[Dict] = None


class ConfigModel(BaseModel):
    uploader: UploaderModel
    plugins: List[PluginModel]
