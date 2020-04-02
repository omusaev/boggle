import logging
import random
import string

from threading import local

request_info = local()


def get_request_id():
    return request_info.id if hasattr(request_info, 'id') else None


def set_request_id(value):
    request_info.id = value


def get_or_generate_request_id():
    request_id = get_request_id()

    if not request_id:
        set_request_id(generate_request_id())

    return request_id


def generate_request_id():
    return ''.join(
        random.choice(string.ascii_uppercase + string.digits)
        for _ in range(12)
    )


class RequestIdLoggingFilter(logging.Filter):
    def filter(self, record):
        request_id = get_request_id() or ''
        record.request_id = request_id

        return True


class RequestIdMiddleware:

    REQUEST_ID_HEADER = 'HTTP_X_REQUEST_ID'

    def __init__(self, app):
        self.app = app

    def __call__(self, environ, start_response):
        request_id = environ.get(self.REQUEST_ID_HEADER, generate_request_id())
        set_request_id(request_id)

        return self.app(environ, start_response)
