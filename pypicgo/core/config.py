import yaml
from pathlib import Path
from typing import ClassVar, Dict, List
from pypicgo.core.models import ConfigModel, PluginModel
from pypicgo.core.utils.modules import import_string
from pypicgo.core.exceptions import ConfigException
from pypicgo import BASE_DIR
from pypicgo.core.logger import logger

template = '''
default:
  uploader: gitee
  plugins:
    - module: pypicgo.plugins.rename.ReNamePlugin
      config:
        format: liunx{hash}chenghaiwen{date}-{filename}
    - module: pypicgo.plugins.typora.TyporaPlugin
    ...

uploaders:
  github:
    module: pypicgo.uploaders.github.uploader.GithubUploader
    config:
      domain: https://api.github.com
      owner: xxx
      repo: xxx
      img_path: xxx
      oauth_token: xxx
    plugins:
      - module: pypicgo.plugins.jsdelivr.JsDelivrPlugin
  ....
'''


class Settings:
    CONFIG_DIR: Path = BASE_DIR
    uploader_class: ClassVar
    uploader_config: Dict
    plugins: List[PluginModel]
    uploader_name: str

    def __init__(self, uploader_name=None):
        self.__init_env()
        self.uploader_name = uploader_name
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
            default = config.get('default', dict())
            common_plugins = default.get('plugins', [])
            try:
                able_uploaders = config['uploaders']
            except KeyError:
                logger.error('No uploader available')
                raise ConfigException('No uploader available')
            
            try:
                default_uploader_name = default['uploader']
            except KeyError:
                logger.error('default uploader is required')
                raise ConfigException('default uploader is required')

            default_uploader = able_uploaders[default_uploader_name]
            if not default_uploader:
                msg = f'not found default uploader {default_uploader_name}'
                logger.error(msg)
                raise ConfigException(msg)
            if self.uploader_name:
                cur_uploader = able_uploaders.get(self.uploader_name, default_uploader)
            else:
                cur_uploader = default_uploader
            uploader_plugins = cur_uploader.get('plugins', [])
            if not uploader_plugins:
                uploader_plugins = []
            plugin_dicts = dict()
            for plugin in common_plugins + uploader_plugins:
                plugin_dicts[plugin['module']] = plugin.get('config')

            plugins = []

            for module, config in plugin_dicts.items():
                plugins.append({
                    'module': module,
                    'config': config
                })
            model = ConfigModel(uploader=cur_uploader, plugins=plugins)
            try:
                module = model.uploader.module
                self.uploader_class = import_string(module)
            except ImportError:
                msg = f'uploader {module} doesnt look like a module path'
                logger.error(msg)
                raise ImportError(msg)
            self.uploader_config = model.uploader.config
            self.plugins = model.plugins
