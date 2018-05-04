from functools import wraps


def add_tag(header):
    def add_tag_decorated(decorated_function):
        @wraps(decorated_function)
        def wrapper(*args, **kwargs):
            return "<{0}>{1}</{0}>".format(header,
                                           decorated_function(*args, **kwargs))
        return wrapper
    return add_tag_decorated


@add_tag('h1')
def print_tagged(text):
    if not isinstance(text, str):
        raise TypeError('Input must be a string')
    return text


def validate_json(*args):
    def true_decorator(decorated_function):
        def wrapper(*args):
            for json in (args):

