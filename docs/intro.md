`PyPicGo`[https://github.com/AnsGoo/PyPicGo] 是一款便捷、易用、扩展性强的命令行图床软件，参考了[PicGo](https://github.com/PicGo/PicGo-Core)的设计，并支持`插件系统`。

目前对`github`、`gitee`和`七牛云`三个免费图床进行了适配，非免费图床以插件包的形式进行适配；支持对图片上传前后的操作，例如`重命名`、`压缩`、`复制剪贴板`、`typora`等插件，你可以采用`PyPicGo`对更多的图床进行支持，及其开发更炫酷的插件

## PicGo原理图

<div align=center>
<img src="https://gitee.com/Ranger313/pbed/raw/master/img/ce9da59dc0436393cd8cca6b66a14f7d-image-20210811084828473-07add3.png"/>
</div>

## 上传器`Uploader`

上传器是处理图片和图床服务器交互的工具，目前官方支持的图床有`gitee`、`github`、`七牛云`


### 支持的图床

|图床名|模块地址|
|---|--|
| `gitee`|`pypicgo.uploaders.gitee.uploader.GiteeUploader`|
| `七牛云`|`pypicgo.uploaders.github.uploader.QiNiuUploader`|
| `github`|`pypicgo.uploaders.qiniu.uploader.GithubUploader`|
| `SM.MS`|`pypicgo.uploaders.smms.uploader.SmmsUploader`|

## 插件 `Plugin`

插件为上传器提供了更丰富和多样化的图片操作支持，按照图片上传的时间段我们把插件分为三种类型`Before`、`After`和`Final`分别代表插件的激活时机,`上传前`、`上传后`和`上传结束`。

### 支持的插件

|插件名称|用途|windows|linux|mac|
|--|--|--|--|--|
|rename|上传前重命名图片|支持|支持|支持|
|notify|上传成功失败的系统通知|支持|支持|支持|
|typora|typora编辑器支持|支持|支持|支持|
|compress|图片上传前压缩|支持|支持|支持|
|jsdelive|github CDN加速|支持|支持|支持|

每种类型的插件配置具体详见插件说明

## 配置

配置文件位于`/$HOME/.PyPicGo/config.yml`目录下，采用`YAML`的方式进行配置。必须配置上传器`uploader`,插件`plugins`的数量可选

```yaml

## 安装

```shell
pip install pypicgo
```

## 配置

配置文件位于`/$HOME/.PyPicGo/config.yml`目录下，采用`YAML`的方式进行配置。必须配置上传器`uploader`,插件`plugins`的数量可选

```yaml
default: # 默认配置
  uploader: gitee # 默认图床
  plugins: # 全局插件
    - module: pypicgo.plugins.rename.ReNamePlugin # 图床插件加载地址
      config:
        format: liunx{hash}chenghaiwen{date}-{filename}
    - module: pypicgo.plugins.typora.TyporaPlugin
    - module: pypicgo.plugins.compress.CompressPlugin
    - module: pypicgo.plugins.notify.NotifyPlugin

uploaders: # 可用图床
  smms: # sm.ms图床配置
    module: pypicgo.uploaders.smms.uploader.SmmsUploader
    config:
      secret_token:  xxx
  gitee: # gitee 图床配置
    module: pypicgo.uploaders.gitee.uploader.GiteeUploader
    config:
      domain: https://gitee.com
      owner: xxx
      repo: xxx
      img_path: xxx
      access_token: xxx
    plugins:
  github: # github图床配置
    module: pypicgo.uploaders.github.uploader.GithubUploader
    config:
      domain: https://api.github.com
      owner: xxx
      repo: xxx
      img_path: xxx
      oauth_token: xxx
    plugins: # github 图床私有插件
      - module: pypicgo.plugins.jsdelivr.JsDelivrPlugin 
  qiniu: #七牛云图床配置
      moduele: pypicgo.uploaders.qiniu.uploader.QiNiuUploader
      config:
        domain: http://demo.pypicho.com/
        bucket_name: pypicgo
        apis:
        - http://up-z1.qiniup.com
        access_key: xxx
        secret_key:  xxxx
```

更多的配置说明参考文档

## 使用

- 帮助信息

```shell
pypicgo -h
```

- 上传文件

```shell
pypicgo -f picture1 picture2 ...
```

- 指定上传图床

```shell
pypicgo -n github -f picture1 picture2 ...
```

如果系统找不到`pypicgo`，请检查`python`的`Scripts`文件夹是否被加入`Path`环境变量



```
- `default.uploader`: 默认上传图床
- `default.uploader`: 全局插件
- `uploaders`: 可用图床配置

**Note:** 图床插件私有插件优先级大于全局插件

更多的配置说明参考文档
