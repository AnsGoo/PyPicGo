import sys
import platform
from typing import List
from pypicgo.core.base.plugin import FinallyPlugin
from pypicgo.core.base.result import Result


class TyporaPlugin(FinallyPlugin):
    name = 'Typora'

    def execute(self, results: List[Result]):
        system_name = platform.system().lower()
        messages = []
        for result in results:
            if result.status:
                messages.append(result.message)
        if len(messages) > 0:
            if system_name == 'darwin':
                message = '\r'.join(messages)
                sys.stdout.write(f'Upload Success:\r{message}\r')
            elif system_name == 'linux':
                message = '\n'.join(messages)
                sys.stdout.write(f'Upload Success:\n{message}\n')
            elif system_name == 'windows':
                message = '\r\n'.join(messages)
                sys.stdout.write(f'Upload Success:\r\n{message}\r\n')

