import argparse

from pypicgo.core.config import Settings
from pypicgo.core.execute import create_uploader
from pypicgo.core.logger import logger


def action():

    parser = argparse.ArgumentParser(
        prog='PyPicGo',
        add_help=True, 
        description='Welcom to PyPicGo'
        )
    parser.add_argument('-n', '--name', type=str, help="uploader name", metavar="github")
    parser.add_argument('-f', '--files', nargs='+', required=True, type=str, help="upload files list", metavar="./img.png")
    args = parser.parse_args()
    uploader_name = args.name
    files = args.files
    settings = Settings(uploader_name=uploader_name)
    uploader = settings.uploader_class
    uploader_config = settings.uploader_config
    plugins = settings.plugins
    with create_uploader(uploader, uploader_config, plugins) as uploader:
        logger.info('upload start')
        for filepath in files:
            logger.info(f'upload file [{filepath}]')
            uploader.do(filepath)
        logger.info('all file has been handled')


if __name__ == '__main__':
    action()
