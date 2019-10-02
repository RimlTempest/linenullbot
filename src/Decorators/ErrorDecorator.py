def Err_tag(tag):
    def _Err_tag(func):
        def wrapper(*args, **kwargs):
            res = '<' + tag + '>'
            res = res + func(*args, **kwargs)
            res = res + '</' + tag + '>'
            return res

        return wrapper

    return _Err_tag
