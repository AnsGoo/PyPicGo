from core.base.plugin import AfterPlugin
from core.notify import PyNotify
from core.base.result import Result


class NotifyPlugin(AfterPlugin):
    name = 'Notify'

    def execute(self, result:Result):
        filename = result.file.origin_file.name
        filepath = result.file.tempfile.resolve()
        if result.status:
            title = 'PyPicGo 上传成功'
            message = f'{filename} 上传成功'
            PyNotify(title, message=message, filepath=filepath).push()
        else:
            title = 'PyPicGo 上传失败'
            message = f'{filename} 上传失败:{result}'
            PyNotify(title, message=message, filepath=filepath).push()
