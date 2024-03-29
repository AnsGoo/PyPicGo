class BaseException(Exception):
    pass


class NotImplementedException(BaseException):

    def __str__(self):
        return 'Mthod is not implemented'


class NotExtendsException(BaseException):

    def __str__(self):
        return 'base class  is not Extends'


class PathNotExistsException(BaseException):
    def __str__(self):
        return 'the path  is not exists'


class IsNotFileException(BaseException):

    def __str__(self):
        return 'the path is not file'


class UploaderTypeException(BaseException):

    def __str__(self):
        return 'not is UploaderPlugin type'


class PluginExecuteException(BaseException):

    def __str__(self):
        return 'Plugin execute exception'


class ConfigException(BaseException):
    
    def __init__(self,message, *args: object) -> None:
        self.message = message
        super().__init__(*args)

    def __str__(self):
        return self.message
