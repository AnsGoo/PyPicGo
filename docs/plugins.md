# 插件 `Plugin`

插件为上传器提供了更丰富和多样化的图片操作支持，按照图片上传的时间段我们把插件分为三种类型`Before`、`After`和`Final`分别代表插件的执行时机,`上传前`、`上传后`和`上传结束`。

相同的类型的插件按照配置的顺序依次执行。

## 配置

```yaml
uploader:
  name: gitee # 图传名称
  module: pypicgo.uploaders.gitee.uploader.GiteeUploader # 上传插件模块
  config: # 上传插件初始化配置
   
plugins: # 插件列表
  - module: pypicgo.plugins.rename.ReNamePlugin # 插件模块
    config:

```

在`plugins`中启用你需要插件，插件按需启用，插件越多上传速度越慢,

- `module`: 插件引用位置
- `config`: 插件配置


## 支持的插件

|插件名称|用途|windows|linux|mac|
|--|--|--|--|--|
|rename|上传前重命名图片|支持|支持|支持|
|notify|上传成功失败的系统通知|支持|支持|支持|
|typora|typora编辑器支持|支持|支持|支持|
|compress|图片上传前压缩|支持|支持|支持|
|clipboard|图片上传完成路劲写入剪切板|支持|支持|支持|

## `Rename`

- 类型： `Before`
- 描述： 图片上传前重命名
- 引用位置： `pypicgo.plugins.rename.ReNamePlugin`



### 配置

```yaml
plugins:
  - module: pypicgo.plugins.rename.ReNamePlugin
    config:
      format: liunx{hash}chenghaiwen{date}-{filename}
```

配置说明：

- `format`: 文件上传命名格式

其中大括号括起来的为文件名变量

支持的文件名变量有：
- `hash`: 32位文件MD5值
- `date`: 时间戳: `%Y%m%d%H%M%S`
- `location`: 文件路径
- `filename`: 原文件名


## `Notify`

- 类型： `After`
- 描述： 图片上传完成之后的通知
- 引用位置： `pypicgo.plugins.notify.NotifyPlugin`



### 配置

```yaml
plugins:
  - module: pypicgo.plugins.notify.NotifyPlugin
```

配置说明：

- 无配置参数

## `Clipboard`
`

- 类型： `After`
- 描述： 图片上传完成后将上传后的地址写入剪切板
- 引用位置： `pypicgo.plugins.clipboard.ClipBoardPlugin`

### 配置

```yaml
plugins:
  - module: pypicgo.plugins.clipboard.ClipBoardPlugin
```

配置说明：

- 无配置参数


## `Typora`

- 类型： `Final`
- 描述： typora编辑器的支持
- 引用位置： `pypicgo.plugins.typora.TyporaPlugin`



### 配置

```yaml
plugins:
  - module: pypicgo.plugins.typora.TyporaPlugin
```

配置说明：

- 无配置参数

### 编辑器使用说明

配置好`PyPicGo`的配置文件，在插件中激活`typora`插件

`文件` -> `偏好设置`->`图像` ->`上传服务设定`->`选择custom Comand`->`在命令中写入pypicgo`

- 验证： 点击验证图片上传选项，显示验证成功即可


## `compress`

- 类型： `Before`
- 描述： 分辨率不变，画质变的图片压缩
- 引用位置： `pypicgo.plugins.compress.Compress`



### 配置

```yaml
plugins:
  - module: pypicgo.plugins.compress.Compress
```

配置说明：

- 无配置参数


## 自定义插件

根据需要实现的功能在上传图片过程中的时机，分别继承`pypicgo.core.base.plugin.BeforePlugin`、`pypicgo.core.base.plugin.AfterPlugin`和`pypicgo.core.base.plugin.FinallyPlugin`并实现`execute`方法

需要注意的是，`BeforePlugin`、`AfterPlugin`和`FinallyPlugin`三种插件的`execute`方法入参和返回值都不一样，`execute`方法为插件处理逻辑。

|插件类型|入参|返回值|
|--|--|--|
|`BeforePlugin`|UploadFile|UploadFile|
|`AfterPlugin`|Result|None|
|`FinallyPlugin`|List[Result]|None|


## 参数类型说明

### UploadFile (`pypicgo.core.base.file.UploadFile`)

属性

- origin_file: Path对象，原始图片位置对象
- filename： str, 图片最终的上传文件名
- tempfile： Path对象， 图片最终的上传文件位置对象


### Result (`pypicgo.core.base.result.Result`)

属性

- status: bool，是否上传成功，True:成功， False:失败
- file: UploadFile对象
- message: str,上传完成信息，成功：上传完成的远程地址，失败:失败原因
