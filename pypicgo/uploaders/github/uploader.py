import base64
import json
from pypicgo.core.base.result import Result
import requests
from typing import List
from requests import Response
from pypicgo.core.base.uploader import CommonUploader
from pypicgo.core.models import PluginModel
from .schemas import GithubUploaderData
from pypicgo.core.logger import logger


class GithubUploader(CommonUploader):
    name: str = 'githubUploader'
    domain: str = 'https://api.github.com'
    owner: str
    repo: str
    img_path: str
    oauth_token: str

    def __init__(self,
                 owner: str,
                 repo: str,
                 img_path: str,
                 oauth_token: str,
                 plugins: List[PluginModel],
                 **kwargs):
        self.repo = repo
        self.owner = owner
        self.img_path = img_path
        self.oauth_token = oauth_token
        self.plugins = plugins
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

    def upload(self) -> Result:
        filename = self.file.filename
        data = self._get_upload_data().json()
        headers = {'Authorization': f'token  {self.oauth_token}'}

        resp = requests.put(
            url=self._upload_path(filename),
            headers=headers,
            data=json.dumps(data)
        )
        result = self.is_success(resp)
        return result


    def is_success(self, resp: Response) -> Result:
        if resp.status_code == 201:
            origin_resp = resp.json()
            download_url = origin_resp['content']['download_url']
            return Result(
                status=True, 
                file=self.file, 
                message='uload success', 
                remote_url=download_url, 
                origin_resp=origin_resp
                )
        else:
            origin_resp = dict()
            try:
                origin_resp = resp.json()
            except:
                pass
            reason = origin_resp.get('message', 'upload fail')
            logger.warning(f'upload fail, message:{reason}')
            return Result(
                status=False, 
                file=self.file, 
                message=reason,
                )
