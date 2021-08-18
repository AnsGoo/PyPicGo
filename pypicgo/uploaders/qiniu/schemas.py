
from typing import Optional, List
from pydantic import BaseModel
from pypicgo.core.models import PluginModel


class QiNiuUploaderConfig(BaseModel):
    domain: str
    bucket_name: str
    apis: List[str]
    secret_key: str
    access_key: str
    plugins: Optional[List[PluginModel]] = []
