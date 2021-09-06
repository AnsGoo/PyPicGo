import sys, os
from typing import List
from pypicgo.core.base.plugin import FinallyPlugin
from pypicgo.core.base.result import Result


class TyporaPlugin(FinallyPlugin):
    name = 'Typora'

    def execute(self, results: List[Result]):
        urls = []
        for result in results:
            if result.status:
                urls.append(result.remote_url)
        if len(urls) > 0:
            message = os.linesep.join(urls)
            sys.stdout.write(f'Upload Success:{os.linesep}{message}{os.linesep}')
