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
            origin_resp = resp.json()
            result = origin_resp.get('success')
            if result:
                url = origin_resp['data']['url']
                return Result(
                    tatus=True, 
                    file=self.file, 
                    message=url,
                    remote_url=url,
                    origin_resp=origin_resp
                )
                    
            else:
                code = origin_resp.get('code')
                if code and code == 'image_repeated':
                    url = origin_resp.get('images')
                    return Result(
                        status=True, 
                        file=self.file, 
                        message=url,
                        remote_url=url,
                        origin_resp=origin_resp
                        )
                else:
                    reason = origin_resp.get('message')
                    return Result(status=False, file=self.file, message=reason)

        else:
            origin_resp = dict()
            try:
                origin_resp = resp.json()
            except:
                pass
            reason = origin_resp.get('message', 'upload fail')
            logger.warning(f'upload fail, message:{reason}')
            return Result(status=False, file=self.file, message=reason)
