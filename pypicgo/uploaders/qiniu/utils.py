from base64 import urlsafe_b64encode

_BLOCK_SIZE = 1024 * 1024 * 4


def b(data):
    if isinstance(data, str):
        return data.encode('utf-8')
    return data


def s(data):
    if isinstance(data, bytes):
        data = data.decode('utf-8')
    return data


def urlsafe_base64_encode(data):
    """urlsafe的base64编码:
    对提供的数据进行urlsafe的base64编码。规格参考：
    https://developer.qiniu.com/kodo/manual/1231/appendix#1
    Args:
        data: 待编码的数据，一般为字符串
    Returns:
        编码后的字符串
    """
    ret = urlsafe_b64encode(b(data))
    return s(ret)
