# PyPicGo

PyPicGo 是参考[PicGo](https://github.com/PicGo/PicGo-Core)开发的一款图床上传的图传工具，并支持各种插件自定义插件，目前PyPicGo自带了`gitee`和`七牛云`图传，和`rename`、`notify`和`typora`等插件，并支持从`pypi`中下载其他插件和`Uploader`’。


## 支持的图床

- `gitee` 支持
- `七牛云` 支持

## 支持的插件

|插件名称|用途|windows|linux|mac|
|--|--|--|--|--|
|rename|上传前重命名图片|支持|支持|支持|
|notify|上传成功失败的系统通知|支持|待测试|待测试|
|typora|typora编辑器支持|支持|支持|支持|

## 配置文件

配置文件位于`/$HOME/.PyPicGO/config.yml`目录下，采用`YAML`的方式进行配置。

```yaml
uploader:
  name: gitee # 图传名称
  module: uploaders.gitee.uploader.GiteeUploader # 上传插件模块
  config: # 上传插件初始化配置
    domain: https://gitee.com
    owner: PyPicGo
    repo: PyPicGo
    branch: master
    img_path: PyPicGo
    access_token: xxxxxxxxxxxx
plugins: # 插件列表
  - module: plugins.md5.ReNamePlugin # 插件模块
    config: # 插件配置
  - module: plugins.notify.NotifyPlugin
    config:
  - module: plugins.clipboard.ClipBoardPlugin
    config:
  - module: plugins.typora.TyporaPlugin
    config:
```

## `Uploader`上传器

uploader是具体的上传插件，用户需要继承`core.base.uploader.CommonUploader`并实现`upload`和`is_success`方法，然后在配置文件中引用即可.

## 插件系统

PyPicgo支持的插件分为三种`before`、`after`和`final`

|插件类型|运行时间|基类类|示例插件|运行时入参|
|--|--|--|--|--|
|before|在图片上传前运行|`core.base.plugin.BeforePlugin`|rename|File|
|after|在图片上传前运行|`core.base.plugin.AfterPlugin`|notify|Result|
|final|在图片上传前运行|`core.base.plugin.FinallyPlugin`|typora|List[Result]|

如果想自定义插件只要根据要求继承任意一个基类插件,并实现`execute`方法，并在`config.yml`中配置即可使用.