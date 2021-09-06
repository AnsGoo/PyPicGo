from pypicgo.core.base.plugin import AfterPlugin
from pypicgo.core.base.result import Result


class JsDelivrPlugin(AfterPlugin):
    name = 'JsDelivr'

    def execute(self, result: Result):
        remote_url = result.remote_url
        if 'raw.githubusercontent.com' in remote_url:
            img_url = remote_url.replace('raw.githubusercontent.com','cdn.jsdelivr.net/gh')
            args = img_url.split('/')
            front = args[0:6]
            end = args[7:]
            result.remote_url = '/'.join(front + end)
