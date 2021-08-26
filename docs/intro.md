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

每种类型的插件配置具体详见插件说明

## 配置

配置文件位于`/$HOME/.PyPicGO/config.yml`目录下，采用`YAML`的方式进行配置。必须配置上传器`uploader`,插件`plugins`的数量可选

```yaml
uploader:
  name: gitee # 图传名称
  module: pypicgo.uploaders.gitee.uploader.GiteeUploader # 上传插件模块
  config: # 上传插件初始化配置
   
plugins: # 插件列表
  - module: pypicgo.plugins.rename.ReNamePlugin # 插件模块
    config:

```

更多的配置说明参考文档
