import base64
import requests
import yaml
import json
from typing import List, Optional, Tuple
from requests import Response
from pathlib import Path
from requests_toolbelt import MultipartEncoder
from pypicgo.core.base.uploader import CommonUploader
from pypicgo.core.models import PluginModel
from .schemas import GiteeUploaderData, GiteeUploaderConfig
from pypicgo.core.logger import logger


class GiteeUploader(CommonUploader):
    name: str = 'giteeUploader'
    domain: str
    owner: str
    repo: str
    branch: str = 'master'
    img_path: str
    access_token: str

    url = 'https://gitee.com/Ranger313/pbed/raw/master/img/CreateReport.png'

    def __init__(self, domain: str,
                 owner: str,
                 repo: str,
                 img_path: str,
                 access_token: str,
                 plugins: List[PluginModel],
                 branch: Optional[str] = 'master'):

        super().__init__(
            domain=domain,
            owner=owner,
            repo=repo,
            img_path=img_path,
            access_token=access_token,
            plugins=plugins,
            branch=branch
        )

    def load_config(self,
                    domain: str,
                    owner: str,
                    repo: str,
                    img_path: str,
                    access_token: str,
                    branch: Optional[str] = 'master'
                    ):
        self.repo = repo
        self.owner = owner
        self.img_path = img_path
        self.domain = domain
        self.access_token = access_token
        self.branch = branch

        logger.info('load config successfully')

    @property
    def base_url(self):
        return f'{self.domain}/api/v5/repos/{self.owner}/{self.repo}'

    def _upload_path(self, filename):
        return f'{self.base_url}/contents/{self.img_path}/{filename}'

    def _get_upload_data(self) -> GiteeUploaderData:
        with open(self.file.tempfile.resolve(), 'rb') as f:
            base64_data = base64.b64encode(f.read())
            filedata = str(base64_data, encoding='utf-8')
        return GiteeUploaderData(
            access_token=self.access_token,
            content=filedata
        )

    def upload(self) -> Response:
        filename = self.file.filename
        data = json.loads(self._get_upload_data().json())
        form_data = MultipartEncoder(data)
        headers = {'Content-Type': form_data.content_type}
        self.resp = requests.post(
            url=self._upload_path(filename),
            headers=headers,
            data=form_data
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
