from __future__ import (absolute_import, division, print_function)
__metaclass__ = type

from datetime import datetime

from google.protobuf.json_format import MessageToDict


class OperationError(Exception):
    pass


def bool_to_enum(value):
    return 'ENABLED' if value else 'DISABLED'


def message_to_dict(message):
    return MessageToDict(message, including_default_value_fields=True, preserving_proto_field_name=True)
