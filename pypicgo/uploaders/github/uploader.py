import base64
import requests
import json
from typing import List, Optional, Tuple
from requests import Response
from pypicgo.core.base.uploader import CommonUploader
from pypicgo.core.models import PluginModel
from .schemas import GithubUploaderData
from pypicgo.core.logger import logger


class GithubUploader(CommonUploader):
    name: str = 'githubUploader'
    domain: 'https://api.github.com'
    owner: str
    repo: str
    branch: str = 'master'
    img_path: str
    oauth_token: str

    def __init__(self, domain: str,
                 owner: str,
                 repo: str,
                 img_path: str,
                 oauth_token: str,
                 plugins: List[PluginModel],
                 branch: Optional[str] = 'master'):

        super().__init__(
            domain=domain,
            owner=owner,
            repo=repo,
            img_path=img_path,
            oauth_token=oauth_token,
            plugins=plugins,
            branch=branch
        )

    def load_config(self,
                    domain: str,
                    owner: str,
                    repo: str,
                    img_path: str,
                    oauth_token: str,
                    branch: Optional[str] = 'master'
                    ):
        self.repo = repo
        self.owner = owner
        self.img_path = img_path
        self.domain = domain
        self.oauth_token = oauth_token
        self.branch = branch

        logger.info('load config successfully')

    @property
    def base_url(self):
        return f'{self.domain}/repos/{self.owner}/{self.repo}'

    def _upload_path(self, filename):
        return f'{self.base_url}/contents/{self.img_path}/{filename}'

    def _get_upload_data(self) -> GithubUploaderData:
        with open(self.file.tempfile.resolve(), 'rb') as f:
            base64_data = base64.b64encode(f.read())
            filedata = str(base64_data, encoding='utf-8')
        return GithubUploaderData(
            content=filedata
        )

    def upload(self) -> Response:
        filename = self.file.filename
        data = self._get_upload_data().json()
        headers = {'Authorization': f'token  {self.oauth_token}'}

        self.resp = requests.put(
            url=self._upload_path(filename),
            headers=headers,
            data=data
        )
        return self.resp

    def is_success(self, resp: Response) -> Tuple[bool, str]:
        if resp.status_code == 201:
            result = resp.json()['content']['download_url']
            return True, result
        else:
            reason = resp.json().get('message')
            logger.warning(f'upload fail, message:{reason}')
            return False, reason
