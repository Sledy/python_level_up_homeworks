import json
import logging
from functools import wraps
import sys


def add_tag(arg1):
    def real_decorator(function):
        def wrapper(*args):
            return ('<{0}>{1}</{0}>'.format(arg1, function()))
        return wrapper
    return real_decorator


@add_tag('h1')
def write_sth():
    return 'something'


result = write_sth()
print(result)


def validate_json(*args):
    def real_decorator(function):
        def wrapper(json_data):
            data = json.loads(json_data)

            if set(data.keys()).issubset(set(args)):
                return function(json_data)

            else:
                raise ValueError
        return wrapper

    return real_decorator


@validate_json('first_name', 'last_name')
def process_json(json_data):
    return len(json_data)


result = process_json('{"first_name": "James", "last_name": "Bond"}')


logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

handler = logging.StreamHandler(sys.stdout)
logger.addHandler(handler)


def log_this(logger, level, format):
    def real_decorator(function):
        @wraps(function)
        def wrapper(*args, **kwargs):
            result = function(*args, **kwargs)
            logger.info('{0} {1} {2} {3} {4}'
                        .format(format, function.__name__,
                                *args, kwargs, result))
        return wrapper
    return real_decorator


@log_this(logger, level=logging.INFO, format='%s: %s -> %s')
def my_func(a, b, c=None, d=False):
    return 'Wow!'


my_func(1, 2, c=True, d=True)
