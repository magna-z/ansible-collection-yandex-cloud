from __future__ import (absolute_import, division, print_function)
__metaclass__ = type

import json

DOCUMENTATION = """
  name: compute_images
  author: Maxim Zalysin <zalysin.m@gmail.com>
  version_added: "0.1.0"
  short_description: 
  description:
    - This lookup returns the contents from a file on the Ansible controller's file system.
  notes:
    - if read in variable context, the file can be interpreted as YAML if the content is valid to the parser.
  options:
    folder_id:
      type: string
      default: standard-images 
      description: 
    name:
      type: string
      description: 
    hostname:
      type: string
      description: 
    zone_id:
      type: string
      description: 
    platform_id:
      type: string
      description: 
    iam_token:
      type: string
      description: 
    service_account_key:
      type: string
      description: 
    token:
      type: string
      description: 
"""

EXAMPLES = """

"""

RETURN = """

"""

import time
import grpc
import yandexcloud

from google.protobuf.json_format import MessageToDict

from yandex.cloud.compute.v1.disk_pb2 import IPV4, Instance
from yandex.cloud.compute.v1.disk_service_pb2_grpc import InstanceServiceStub
from yandex.cloud.compute.v1.disk_service_pb2 import (
    AttachedDiskSpec,
    CreateInstanceRequest,
    DeleteInstanceRequest,
    GetInstanceRequest,
    ListInstancesRequest,
    NetworkInterfaceSpec,
    OneToOneNatSpec,
    PrimaryAddressSpec,
    ResourcesSpec,
    RestartInstanceRequest,
    StartInstanceRequest,
    StopInstanceRequest,
)

from ansible.module_utils.basic import AnsibleModule
from ansible.module_utils.common.text.converters import to_native
from ansible.module_utils.common.yaml import *


def main():
    module = AnsibleModule(
        argument_spec=dict(
            state=dict(type="str", default="present", choices=["present", "restarted", "stopped", "absent"]),
            folder_id=dict(type="str", required=True),
            name=dict(type="str", required=True),
            hostname=dict(type="str"),
            zone_id = dict(type="str"),
            platform_id = dict(type="str", default="standard-v3"),
            resources=dict(
                type="dict",
                options=dict(
                    memory=dict(type="int", required=True),
                    cores=dict(type="int", required=True),
                    core_fraction=dict(type="int", default=100),
                    gpus=dict(type="int", default=0),
                ),
            ),
            boot_disk=dict(
                type="dict",
                options=dict(
                    auto_delete=dict(type="bool", default=True),
                    type=dict(type="str", choices=["network-hdd", "network-sdd"]),
                    size=dict(type="int", required=True),
                    image_id=dict(type="str", required=True),
                ),
            ),
            network_interfaces=dict(
                type="list",
                elements="dict",
                options=dict(
                    subnet_id=dict(type="str", required=True),
                    public_ip_nat=dict(type="bool", default=True)
                ),
            ),
            metadata=dict(type="dict", default={}),
            iam_token=dict(type="str"),
            token=dict(type="str"),
            service_account_key=dict(type="str"),
        ),
        required_one_of=[["iam_token", "token", "service_account_key"], ["id", "name"]],
        supports_check_mode=False,
    )

    sdk = yandexcloud.SDK(
        interceptor=yandexcloud.RetryInterceptor(max_retry_count=3, retriable_codes=[grpc.StatusCode.UNAVAILABLE]),
        iam_token=module.params["iam_token"],
        token=module.params["token"],
        service_account_key=module.params["service_account_key"]
    )
