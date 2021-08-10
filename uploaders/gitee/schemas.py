import base64
import binascii
from typing import Optional, List
from pydantic import BaseModel, validator, ValidationError

from core.models import PluginModel


class GiteeUploaderData(BaseModel):
    access_token: str
    message: str = 'pyPicGo upload success'
    content: str

    @validator('content')
    def validate_content(cls, content):
        try:
            if base64.b64encode(base64.b64decode(content.encode('utf-8'))) == content.encode('utf-8'):
                return content
            else:
                raise ValidationError('Non-base64 digit found')
        except binascii.Error('Non-base64 digit found'):
            raise ValidationError('Non-base64 digit found')


class GiteeUploaderConfig(BaseModel):
    domain: str
    owner: str
    repo: str
    branch: Optional[str] = 'master'
    img_path: str
    access_token: str
    plugins: Optional[List[PluginModel]] = []
