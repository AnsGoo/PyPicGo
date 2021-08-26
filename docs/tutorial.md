
## 安装

```shell
pip install pypicgo
```

## 配置

配置文件位于`/$HOME/.PyPicGO/config.yml`目录下，采用`YAML`的方式进行配置。必须配置上传器`uploader`,插件`plugins`的数量可选

```yaml
uploader:
  name: gitee # 图传名称
  module: pypicgo.uploaders.gitee.uploader.GiteeUploader # 上传插件模块
  config: # 上传插件初始化配置
    owner: PyPicGo
    repo: PyPicGo
    img_path: PyPicGo
    access_token: xxxxxxxxxxxx
plugins: # 插件列表
  - module: pypicgo.plugins.rename.ReNamePlugin # 插件模块
  - module: pypicgo.plugins.notify.NotifyPlugin
  - module: pypicgo.plugins.clipboard.ClipBoardPlugin
  - module: pypicgo.plugins.typora.TyporaPlugin
```

更多的配置说明参考文档

## 使用

```shell
pypicgo picture1 picture2 ...
```

如果系统找不到`pypicgo`，请检查`python`的`Scripts`文件夹是否被加入`Path`环境变量

