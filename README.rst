PyPicGo
=======

PyPicGo
是一款图床工具,是\ `PicGo <https://github.com/PicGo/PicGo-Core>`__\ PyPicGo
是一款图床工具，是PicGo的Python版实现，并支持各种插件自定义插件，目前\ ``PyPicGo``\ 自带了\ ``gitee``\ 、\ ``github``\ 、\ ``SM.MS``\ 和\ ``七牛云``\ 图传，以及\ ``rename``\ 、\ ``notify``\ 和\ ``typora``\ 等插件，并支持从\ ``pypi``\ 中下载其他插件和Uploader

安装
----

.. code:: shell

    pip install pypicgo

配置
----

配置文件位于\ ``/$HOME/.PyPicGo/config.yml``\ 目录下，采用\ ``YAML``\ 的方式进行配置。必须配置上传器\ ``uploader``,插件\ ``plugins``\ 的数量可选

.. code:: yaml

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

更多的配置说明参考文档

使用
----

-  帮助信息

.. code:: shell

    pypicgo -h

-  上传文件

.. code:: shell

    pypicgo -f picture1 picture2 ...

-  指定上传图床

.. code:: shell

    pypicgo -n github -f picture1 picture2 ...

如果系统找不到\ ``pypicgo``\ ，请检查\ ``python``\ 的\ ``Scripts``\ 文件夹是否被加入\ ``Path``\ 环境变量

\`\`\`

更多的配置说明参考文档

使用
----

.. code:: shell

    pypicgo -n 图床名 -f img1.jpg img2.jpg

支持的图床
----------

+--------------+-------------------------------------------------------+
| 图床名       | 模块地址                                              |
+==============+=======================================================+
| ``gitee``    | ``pypicgo.uploaders.gitee.uploader.GiteeUploader``    |
+--------------+-------------------------------------------------------+
| ``七牛云``   | ``pypicgo.uploaders.github.uploader.QiNiuUploader``   |
+--------------+-------------------------------------------------------+
| ``github``   | ``pypicgo.uploaders.qiniu.uploader.GithubUploader``   |
+--------------+-------------------------------------------------------+
| ``SM.MS``    | ``pypicgo.uploaders.smms.uploader.SmmsUploader``      |
+--------------+-------------------------------------------------------+

支持的插件
----------

+------------+--------------------------+-----------+---------+--------+
| 插件名称   | 用途                     | windows   | linux   | mac    |
+============+==========================+===========+=========+========+
| rename     | 上传前重命名图片         | 支持      | 支持    | 支持   |
+------------+--------------------------+-----------+---------+--------+
| notify     | 上传成功失败的系统通知   | 支持      | 支持    | 支持   |
+------------+--------------------------+-----------+---------+--------+
| typora     | typora编辑器支持         | 支持      | 支持    | 支持   |
+------------+--------------------------+-----------+---------+--------+
| compress   | 图片上传前压缩           | 支持      | 支持    | 支持   |
+------------+--------------------------+-----------+---------+--------+

``Uploader``\ 上传器
--------------------

uploader是具体的上传插件，用户需要继承\ ``pypicgo.core.base.uploader.CommonUploader``\ 并实现\ ``upload``\ 方法，然后在配置文件中引用即可.

插件系统
--------

PyPicgo支持的插件分为三种\ ``before``\ 、\ ``after``\ 和\ ``final``

+------------+------------------------+----------------------------------------------+------------+----------------+
| 插件类型   | 运行时间               | 基类类                                       | 示例插件   | 运行时入参     |
+============+========================+==============================================+============+================+
| before     | 在图片上传前运行       | ``pypicgo.core.base.plugin.BeforePlugin``    | rename     | File           |
+------------+------------------------+----------------------------------------------+------------+----------------+
| after      | 在图片上传后运行       | ``pypicgo.core.base.plugin.AfterPlugin``     | notify     | Result         |
+------------+------------------------+----------------------------------------------+------------+----------------+
| final      | 在所有图片上传后运行   | ``pypicgo.core.base.plugin.FinallyPlugin``   | typora     | List[Result]   |
+------------+------------------------+----------------------------------------------+------------+----------------+

如果想自定义插件只要根据要求继承任意一个基类插件,并实现\ ``execute``\ 方法，并在\ ``config.yml``\ 中配置即可使用.

开发
----

.. code:: shell

    git clone git@github.com:AnsGoo/PyPicGo.git

    cd pypicgo

    pipenv shell

    pipenv install

    python run.py -n 图床名 -f img1.jpg img2.jpg

