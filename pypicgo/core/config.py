import yaml
from pathlib import Path
from typing import ClassVar, Dict, List
from pypicgo.core.models import ConfigModel, PluginModel
from pypicgo.core.utils.modules import import_string
from pypicgo import BASE_DIR

template = '''
uploader:
  name: pypicgo.uploaders.gitee.uploader.GiteeUploader
  module: 
  config:
plugins:
  - module: pypicgo.plugins.rename.ReNamePlugin
'''


class Settings:
    CONFIG_DIR: Path = BASE_DIR
    uploader_class: ClassVar
    uploader_config: Dict
    plugins: List[PluginModel]

    def __init__(self):
        self.__init_env()
        self.load_config()

    def __init_env(self):
        path = self.CONFIG_DIR.joinpath('config.yaml')
        if not path.exists():
            with path.open(mode='w') as f:
                f.write(template)

    def load_config(self):
        config_file = self.CONFIG_DIR.joinpath('config.yaml')
        with open(config_file.resolve(), 'r', encoding='utf-8') as f:
            config = yaml.load(f.read(), Loader=yaml.CFullLoader)
            model = ConfigModel(uploader=config['uploader'], plugins=config.get('plugins', []))
            try:
                module = model.uploader.module
                self.uploader_class = import_string(module)
            except ImportError:
                raise ImportError(f'uploader {module} doesnt look like a module path')
            self.uploader_config = model.uploader.config
            self.plugins = model.plugins
