
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


## `Github`图床:

利用`github`仓库搭建图床是常见的免费图床方式之一，具体搭建方式请自行查阅。

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

配置说明：

- `domain`: 自定义域名，没有可填测试域名，测试域名按月动态变更，不建议
- `bucket_name`: 空间名
- `apis`: 列表，可用的上床地址列表
- `access_key`: AK
- `secret_key`: SK

## 自定义上传器

自定义上传器继承`pypicgo.core.base.uploader.CommonUploader`并重写`load_config`和`upload`,并按需重写`__init__`方法即可，其中`load_config`在初始化参数，在`upload`方法中处理上传图片逻辑，`upload`方法必须返回一个`Result`对象

```python 
from pypicgo.core.base.uploader import CommonUploader


class CustomeUploader(CommonUploader):

    def __init(self,...**kwargs):
        ...
        self.load_config(...)

    def load_config(self,.....):
        ...



    def upload(self) -> Result:
        ...
        return result
```


