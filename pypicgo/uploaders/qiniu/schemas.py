
from typing import Optional, List
from pypicgo.core.models import PluginModel


class QiNiuUploaderConfig:
    domain: str
    bucket_name: str
    apis: List[str]
    secret_key: str
    access_key: str
    plugins: Optional[List[PluginModel]] = []

    def __init__(self,
        domain: str,
        bucket_name: str,
        apis: List[str],
        secret_key: str,
        access_key: str,
        plugins: Optional[List[PluginModel]] = []
    ) -> None:
        self.domain = domain
        self.bucket_name = bucket_name
        self.apis = apis
        self.access_key = access_key
        self.secret_key = secret_key
        self.plugins = plugins
