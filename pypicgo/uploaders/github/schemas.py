import base64
import binascii
from typing import Optional, List
from pydantic import BaseModel, validator, ValidationError
from pypicgo.core.models import PluginModel


class GithubUploaderData(BaseModel):
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


class GithubUploaderConfig(BaseModel):
    owner: str
    repo: str
    img_path: str
    oauth_token: str
    plugins: Optional[List[PluginModel]] = []
