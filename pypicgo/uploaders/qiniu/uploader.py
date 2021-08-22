import requests
import json
import random
import hmac
import time
from hashlib import sha1
from typing import List, Optional, Dict
from requests import Response
from pypicgo.core.base.uploader import CommonUploader
from pypicgo.core.models import PluginModel
from pypicgo.core.base.result import Result
from pypicgo.core.logger import logger
from .utils import urlsafe_base64_encode

_policy_fields = set(
    'callbackUrl',  # 回调URL
    'callbackBody',  # 回调Body
    'callbackHost',  # 回调URL指定的Host
    'callbackBodyType',  # 回调Body的Content-Type
    'callbackFetchKey',  # 回调FetchKey模式开关
    'returnUrl',  # 上传端的303跳转URL
    'returnBody',  # 上传端简单反馈获取的Body
    'endUser',  # 回调时上传端标识
    'saveKey',  # 自定义资源名
    'forceSaveKey',  # saveKey的优先级设置。为 true 时，saveKey不能为空，会忽略客户端指定的key，强制使用saveKey进行文件命名。参数不设置时，默认值为false
    'insertOnly',  # 插入模式开关
    'detectMime',  # MimeType侦测开关
    'mimeLimit',  # MimeType限制
    'fsizeLimit',  # 上传文件大小限制
    'fsizeMin',  # 上传文件最少字节数
    'persistentOps',  # 持久化处理操作
    'persistentNotifyUrl',  # 持久化处理结果通知URL
    'persistentPipeline',  # 持久化处理独享队列
    'deleteAfterDays',  # 文件多少天后自动删除
    'fileType',  # 文件的存储类型，0为普通存储，1为低频存储
    'isPrefixalScope'  # 指定上传文件必须使用的前缀
)


class QiNiuUploader(CommonUploader):
    name: str = 'giteeUploader'
    domain: str = ''
    apis: List = []
    access_key: str = ''
    secret_key: bytes = b''
    bucket_name: str = ''

    url = 'https://gitee.com/Ranger313/pbed/raw/master/img/CreateReport.png'

    def __init__(self, domain: str,
                 bucket_name: str,
                 apis: List[str],
                 access_key: str,
                 secret_key: str,
                 plugins: Optional[List[PluginModel]] = [],
                 **kwargs):
        super().__init__(
            bucket_name=bucket_name,
            apis=apis,
            access_key=access_key,
            domain=domain,
            secret_key=secret_key.encode('utf-8'),
            plugins=plugins,
            **kwargs

        )

    def load_config(self,
                    domain: str,
                    bucket_name: str,
                    apis: List[str],
                    access_key: str,
                    secret_key: bytes,
                    **kwargs
                    ):
        self.bucket_name = bucket_name
        self.apis = apis
        self.access_key = access_key
        self.domain = domain
        self.secret_key = secret_key
        logger.info('init settings successfully')

    @property
    def api(self):
        return random.choice(self.apis)

    def __token(self, data):
        hashed = hmac.new(self.secret_key, data.encode('utf-8'), sha1)
        return urlsafe_base64_encode(hashed.digest())

    def __token_with_data(self, data):
        data = urlsafe_base64_encode(data)
        return '{0}:{1}:{2}'.format(
            self.access_key, self.__token(data), data)

    def get_token(self, bucket: str, policy: Dict, expires: int = 3600):
        if bucket is None or bucket == '':
            raise ValueError('invalid bucket name')
        args = {
            'scope': bucket,
            'deadline': int(time.time()) + expires
        }
        for k, v in policy.items():
            if k in _policy_fields:
                args[k] = v
        data = json.dumps(args, separators=(',', ':'))
        return self.__token_with_data(data)

    def upload(self) -> Result:
        fields = dict()
        filename = self.file.filename
        token = self.get_token(self.bucket_name, {'fileType': 1})
        fields['token'] = token
        fields['key'] = filename
        with open(self.file.tempfile.resolve(), 'rb') as f:
            resp = requests.post(
                url=self.api,
                data=fields,
                files={'file': ('file_name', f, 'application/octet-stream')}
            )

        result = self.is_success(resp=resp)
        return result

    def is_success(self, resp: Response) -> Result:
        if resp.status_code == 200:
            key = resp.json()['key']
            remote_file = f'{self.domain}{key}'
            return Result(status=True, file=self.file, message=remote_file)
        else:
            reason = resp.text
            try:
                reason = resp.json().get('error')
            except:
                pass
            logger.warning(f'upload fail, message:{reason}')
            return Result(status=False, file=self.file, message=reason)
