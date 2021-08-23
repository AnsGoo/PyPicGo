import requests
from typing import List
from requests import Response
from pypicgo.core.base.result import Result
from pypicgo.core.base.uploader import CommonUploader
from pypicgo.core.models import PluginModel
from pypicgo.core.logger import logger


class SmmsUploader(CommonUploader):
    name: str = 'SmmsbUploader'
    domain: str = 'https://sm.ms/api/v2'
    secret_token: str

    def __init__(self, secret_token: str,
                 plugins: List[PluginModel],
                 **kwargs):

        super().__init__(
            secret_token=secret_token,
            plugins=plugins,
            **kwargs
        )

    def load_config(self,
                   secret_token: str,
                    **kwargs
                    ):
        self.secret_token =  secret_token

        logger.info('load config successfully')

    @property
    def upload_url(self):
        return f'{self.domain}/upload/'


    def upload(self) -> Result:
        files = {
            'smfile': open(self.file.tempfile.resolve(), 'rb'),
        }
        headers = {'Authorization': f'{self.secret_token}'}

        resp = requests.post(
            url=self.upload_url,
            headers=headers,
            files= files,
        )
        result = self.is_success(resp)
        return result


    def is_success(self, resp: Response) -> Result:
        if resp.status_code == 200:
            url = resp.json()['data']['url']
            return Result(status=True, file=self.file, message=url)
        else:
            reason = resp.json().get('message')
            logger.warning(f'upload fail, message:{reason}')
            return Result(status=False, file=self.file, message=reason)
