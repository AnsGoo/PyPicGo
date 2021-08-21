from pypicgo.core.base.plugin import AfterPlugin
from .tk import TkinterNotice
from pypicgo.core.base.result import Result


class NotifyPlugin(AfterPlugin):
    name = 'Notify'

    def execute(self, result: Result):
        message = result.message
        if result.status:
            message = f'{result.file.origin_file.name} 已上传成功'
        filepath = result.file.tempfile.resolve()
        TkinterNotice().send(result.status, message, filepath)
