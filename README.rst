PyPicGo
=======

PyPicGo
是参考\ `PicGo <https://github.com/PicGo/PicGo-Core>`__\ 开发的一款图床上传的图传工具，并支持各种插件自定义插件，目前PyPicGo自带了\ ``gitee``\ 、\ ``github``\ 和\ ``七牛云``\ 图传，和\ ``rename``\ 、\ ``notify``\ 和\ ``typora``\ 等插件，并支持从\ ``pypi``\ 中下载其他插件和\ ``Uploader``\ 。

安装
----

.. code:: shell

    pip install pypicgo

配置
----

配置文件位于\ ``/$HOME/.PyPicGO/config.yml``\ 目录下，采用\ ``YAML``\ 的方式进行配置。必须配置上传器\ ``uploader``,插件\ ``plugins``\ 的数量可选

.. code:: yaml

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
        config: # 插件配置
      - module: pypicgo.plugins.notify.NotifyPlugin
      - module: pypicgo.plugins.clipboard.ClipBoardPlugin
      - module: pypicgo.plugins.typora.TyporaPlugin

更多的配置说明参考文档

使用
----

.. code:: shell

    pypicgo xxx.jpg

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

    python run.py  xxx.jpg

