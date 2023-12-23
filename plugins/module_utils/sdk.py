from __future__ import (absolute_import, division, print_function)
__metaclass__ = type

from grpc import StatusCode
from yandexcloud import (SDK, RetryInterceptor)

MAX_RETRY_COUNT = 3
PER_CALL_TIMEOUT = 10
RETRIABLE_CODES = [StatusCode.UNAVAILABLE]


def client(service, **kwargs):
    return SDK(
        interceptor=RetryInterceptor(
            max_retry_count=MAX_RETRY_COUNT,
            per_call_timeout=PER_CALL_TIMEOUT,
            retriable_codes=RETRIABLE_CODES,
        ),
        **kwargs,
    ).client(service)
