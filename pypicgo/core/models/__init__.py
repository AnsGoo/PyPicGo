from pydantic import BaseModel, ValidationError, validator
from typing import Dict, Optional, List
from pypicgo.core.utils.modules import  import_string


class PluginModel(BaseModel):
    module: str
    config: Optional[Dict] = None

    @validator('module')
    def check_module(cls, value) -> str:
        if isinstance(value, str):
            try:
                import_string(value)
                return value
            except ImportError:
                raise ValidationError(f'{value} doesnt look like a module path')
        else:
            raise ValidationError('module must string')


class UploaderModel(BaseModel):
    name: str
    module: str
    config: Optional[Dict] = None

    @validator('module')
    def check_module(cls, value) -> str:
        if isinstance(value, str):
            try:
                import_string(value)
                return value
            except ImportError:
                raise ValidationError(f'{value} doesnt look like a module path')
        else:
            raise ValidationError('module must string')




class ConfigModel(BaseModel):
    uploader: UploaderModel
    plugins: List[PluginModel]