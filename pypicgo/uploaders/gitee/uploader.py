import base64
import requests
import json
from typing import List, Optional, Tuple
from requests import Response
from requests_toolbelt import MultipartEncoder
from pypicgo.core.base.uploader import CommonUploader
from pypicgo.core.models import PluginModel
from pypicgo.core.base.result import Result
from .schemas import GiteeUploaderData
from pypicgo.core.logger import logger


class GiteeUploader(CommonUploader):
    name: str = 'giteeUploader'
    domain: str = 'https://gitee.com'
    owner: str
    repo: str
    img_path: str
    access_token: str

    def __init__(self,
                 owner: str,
                 repo: str,
                 img_path: str,
                 access_token: str,
                 plugins: List[PluginModel],
                 **kwargs
                 ):

        super().__init__(
            owner=owner,
            repo=repo,
            img_path=img_path,
            access_token=access_token,
            plugins=plugins,
            **kwargs
        )

    def load_config(self,
                    owner: str,
                    repo: str,
                    img_path: str,
                    access_token: str,
                    **kwargs
                    ):
        self.repo = repo
        self.owner = owner
        self.img_path = img_path
        self.access_token = access_token

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

    def upload(self) -> Result:
        filename = self.file.filename
        data = json.loads(self._get_upload_data().json())
        form_data = MultipartEncoder(data)
        headers = {'Content-Type': form_data.content_type}
        resp = requests.post(
            url=self._upload_path(filename),
            headers=headers,
            data=form_data
        )
        result = self.is_success(resp)

        return result

    def is_success(self, resp: Response) -> Result:
        if resp.status_code == 201:
            download_url = resp.json()['content']['download_url']
            return Result(status=True, file=self.file, message=download_url)
        else:
            reason = resp.json().get('message')
            logger.warning(f'upload fail, message:{reason}')
            return Result(status=False, file=self.file, message=reason)
