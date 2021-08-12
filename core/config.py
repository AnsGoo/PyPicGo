import os
import platform
import yaml
from pathlib import Path
from typing import ClassVar, Dict, List
from core.models import ConfigModel, PluginModel
from core.utils.modules import import_string

template = '''
uploader:
  name: gitee
  module: 
  config:
plugins:
  - module: plugins.rename.ReNamePlugin
'''
system_name = platform.system().lower()

if system_name == 'linux':
    HOME = os.environ.get('HOME')
    home = Path(HOME)
    
elif system_name == 'windows':
    HOMEDRIVE = os.environ.get('HOMEDRIVE')
    HOME = os.environ.get('HOMEPATH')
    home = Path(HOMEDRIVE).joinpath(HOME)
BASE_DIR = home.joinpath('.PyPicGO')
if not BASE_DIR.exists():
    BASE_DIR.mkdir(parents=True)

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
            model = ConfigModel(**config)
            self.uploader_class = import_string(model.uploader.module)
            self.uploader_config = model.uploader.config
            self.plugins = model.plugins





