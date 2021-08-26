import tempfile
import requests
from typing import List
from pathlib import Path
from requests import Response
from pypicgo.core.base.result import Result
from pypicgo.core.base.uploader import CommonUploader
from pypicgo.core.models import PluginModel
from pypicgo.core.logger import logger

BASE_DIR = Path(__file__).resolve().parent


class SmmsUploader(CommonUploader):
    name: str = 'SmmsbUploader'
    domain: str = 'https://sm.ms/api/v2'
    secret_token: str

    def __init__(self, secret_token: str,
                 plugins: List[PluginModel],
                 **kwargs):

        self.secret_token =  secret_token
        self.plugins = plugins
        logger.info('load config successfully')    

    @property
    def upload_url(self):
        return f'{self.domain}/upload/'


    def upload(self) -> Result:
        tempfile = BASE_DIR.joinpath(self.file.filename)
        with open(self.file.tempfile.resolve(), 'rb') as f:
            with open(tempfile.resolve(),'wb') as ft:
                ft.write(f.read())
        self.file.tempfile = tempfile
        file = open(self.file.tempfile.resolve(), 'rb')
        files = {
            'smfile': file,
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
            data = resp.json()
            result = data.get('success')
            if result:
                url = resp.json()['data']['url']
                return Result(status=True, file=self.file, message=url)
            else:
                code = data.get('code')
                if code and code == 'image_repeated':
                    url = data.get('images')
                    return Result(status=True, file=self.file, message=url)
                else:
                    reason = data.get('message')
                    return Result(status=False, file=self.file, message=reason)

        else:
            reason = resp.json().get('message')
            logger.warning(f'upload fail, message:{reason}')
            return Result(status=False, file=self.file, message=reason)
