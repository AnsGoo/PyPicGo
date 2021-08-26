
# 上传器`Uploader`

上传器是处理图片和图床服务器交互的工具，目前官方支持的图床有`gitee`、`github`、`七牛云`

```yaml
uploader:
  name: gitee
  module: pypicgo.uploaders.gitee.uploader.GiteeUploader
  config:

```

- `name`:图床名，可选
- `module`: 图床引用位置
- `config`: 图床配置参数

## `Gitee`图床:

利用`gitee`仓库搭建图床是常见的免费图床方式之一，具体搭建方式请自行查阅。

### 模块引用位置

`pypicgo.uploaders.gitee.uploader.GiteeUploader`


### 配置

```yaml
uploader:
  name: gitee
  module: pypicgo.uploaders.gitee.uploader.GiteeUploader
  config:
    owner: Ranger313
    repo: pbed
    img_path: PyPicGo
    access_token: xxx
```

配置说明：

- `owner`: gitee用户名
- `repo`: git仓名
- `img_path`: 默认图片上传文件夹
- `access_token`: gitee token


## `Github`图床:

利用`github`仓库搭建图床是常见的免费图床方式之一，具体搭建方式请自行查阅。

### 模块引用位置

`pypicgo.uploaders.github.uploader.GithubUploader`


### 配置

```yaml
uploader:
  name: gitee
  module: pypicgo.uploaders.github.uploader.GithubUploader
  config:
    owner: ansgoo
    repo: pbed
    img_path: PyPicGo
    oauth_token:  xxx
```

配置说明：

- `owner`: github用户名
- `repo`: git仓名
- `img_path`: 默认图片上传文件夹
- `oauth_token`: gitee token


## `七牛云`图床:

七牛云是国内云存储服务商之一，免费用户提供`10G`存储空间以及`10G/月`的CDN回流流量，长期使用需要绑定自己的域名，默认是测试域名，有效期为1个月。

### 模块引用位置

`pypicgo.uploaders.qiniu.uploader.QiNiuUploader`


### 配置

```yaml
uploader:
  name: qiniu
  moduele: pypicgo.uploaders.qiniu.uploader.QiNiuUploader
  config:
    domain: http://demo.pypicho.com/
    bucket_name: pypicgo
    apis:
      - http://up-z1.qiniup.com
    access_key: xxx
    secret_key:  xxxx
```
## `SM.MS`图床:

`SM.MS` 是一款知名的图床服务，免费提供`5G`存储空间,单张图片不能超过`5M`,支持`API`访问

### 模块引用位置

`pypicgo.uploaders.smms.uploader.SmmsUploader`


### 配置

```yaml
uploader:
  name: smms
  module: pypicgo.uploaders.smms.uploader.SmmsUploader
  config:
    secret_token:  xxx
```

配置说明：

- `secret_token`: SM.MS 图床Token

**Notice:**: `SM.MS` 图床不支持自定义文件名，`SM.M`S图床的文件名是以服务器的对该张图生成的`Hash`码为准，因此`rename`插件对该图床其实不生效

## 自定义上传器

自定义上传器继承`pypicgo.core.base.uploader.CommonUploader`,重写`upload`,并按需重写`__init__`方法即可，`upload`方法为处理上传图片逻辑，`upload`方法必须返回一个`Result`对象

```python 
from pypicgo.core.base.uploader import CommonUploader


class CustomeUploader(CommonUploader):

    def __init(self,...**kwargs):
        ...

    def upload(self) -> Result:
        ...
        return result
```
