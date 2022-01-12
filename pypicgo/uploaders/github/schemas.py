import base64
from typing import Optional, List
from pypicgo.core.models import PluginModel


class GithubUploaderData:
    message: str = 'pyPicGo upload success'
    content: str

    def __init__(self, content:str) -> None:
        try:
            if base64.b64encode(base64.b64decode(content.encode('utf-8'))) == content.encode('utf-8'):
                self.content = content
            else:
                raise ValueError('Non-base64 digit found')
        except ValueError:
            raise ValueError('Non-base64 digit found')

    def json(self):
        return {
            'message':self.message,
            'content': self.content
        }


class GithubUploaderConfig:
    owner: str
    repo: str
    img_path: str
    oauth_token: str
    plugins: Optional[List[PluginModel]] = []


    def __init__(self,
        owner:str,
        repo:str,
        img_path:str,
        oauth_token:str,
        plugins: Optional[List[PluginModel]] = []):
        self.owner = owner
        self.repo = repo
        self.img_path = img_path
        self.oauth_token = oauth_token
        self.plugins = plugins
