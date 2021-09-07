
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

