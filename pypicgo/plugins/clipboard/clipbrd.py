import pyperclip
from pypicgo.core.logger import logger


class ClipBoard:

    @classmethod
    def read(self):
        pass

    @classmethod
    def writer(self, data: str):
        pyperclip.copy(data)
        logger.info(f'writer to ClipBoard: {data}')
