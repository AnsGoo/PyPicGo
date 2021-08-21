import sys
from pypicgo.core.config import Settings
from pypicgo.core.execute import create_uploader
from pypicgo.core.logger import logger


def action():
    argv = sys.argv
    if len(argv) == 1:
        logger.info('PyPicGo has been installed successfully')
    elif len(argv) > 1:
        settings = Settings()
        uploader = settings.uploader_class
        uploader_config = settings.uploader_config
        plugins = settings.plugins
        with create_uploader(uploader, uploader_config, plugins) as uploader:
            files = argv[1:]
            for filepath in files:
                uploader.do(filepath)


if __name__ == '__main__':
    action()
