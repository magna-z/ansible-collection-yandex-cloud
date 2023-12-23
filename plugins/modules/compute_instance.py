from __future__ import (absolute_import, division, print_function)
__metaclass__ = type

import json

DOCUMENTATION = """
  name: compute_images
  author: Maxim Zalysin <zalysin.m@gmail.com>
  version_added: "0.1.0"
  short_description: 
  description:
    - ...
  notes:
    - ...
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

from yandex.cloud.compute.v1.instance_pb2 import IPV4, Instance
from yandex.cloud.compute.v1.instance_service_pb2_grpc import InstanceServiceStub
from yandex.cloud.compute.v1.instance_service_pb2 import (
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


def _find(module, sdk):
    result = {}

    folder_id = module.params["folder_id"]
    filter = "name = \"%s\"" % module.params["name"]

    service = sdk.client(InstanceServiceStub)

    try:
        service_return = MessageToDict(service.List(ListInstancesRequest(
            folder_id=folder_id,
            filter=filter
        )))

        if "instances" in service_return:
            result = service_return["instances"][0]

    except Exception as e:
        module.fail_json(
            msg="unknown error listing instances in folder id %r by filter %r. Error was: %s"
            % (to_native(folder_id), to_native(filter), to_native(e))
        )

    return result


def _get(module, sdk, instance_id):
    result = {}

    service = sdk.client(InstanceServiceStub)
    try:
        service_return = service.Get(GetInstanceRequest(instance_id=instance_id))
        result = MessageToDict(service_return)
    except Exception as e:
        module.fail_json(
            msg="unknown error getting instance by id %r. Error was: %s" % (to_native(instance_id), to_native(e))
        )

    return result


def _create(module, sdk):
    result = {}

    network_interface_specs = []
    for network_interface in module.params["network_interfaces"]:
        network_interface_specs.append(
            NetworkInterfaceSpec(
                subnet_id=network_interface["subnet_id"],
                primary_v4_address_spec=PrimaryAddressSpec(
                    one_to_one_nat_spec=OneToOneNatSpec(ip_version=IPV4) if network_interface["public_ip_nat"] else None
                ),
            ),
        )

    request = CreateInstanceRequest(
        folder_id=module.params["folder_id"],
        name=module.params["name"],
        hostname=module.params["hostname"],
        resources_spec=ResourcesSpec(
            memory=module.params["resources"]["memory"],
            gpus=module.params["resources"]["gpus"],
            cores=module.params["resources"]["cores"],
            core_fraction=module.params["resources"]["core_fraction"],
        ),
        zone_id=module.params["zone_id"],
        platform_id=module.params["platform_id"],
        boot_disk_spec=AttachedDiskSpec(
            auto_delete=module.params["boot_disk"]["auto_delete"],
            disk_spec=AttachedDiskSpec.DiskSpec(
                type_id=module.params["boot_disk"]["type"],
                size=module.params["boot_disk"]["size"],
                image_id=module.params["boot_disk"]["image_id"],
            ),
        ),
        network_interface_specs=network_interface_specs,
        metadata=module.params["metadata"],
    )

    service = sdk.client(InstanceServiceStub)

    try:
        service_return = service.Create(request)
        result = MessageToDict(service_return)
    except Exception as e:
        module.fail_json(
            msg="unknown error create instance %r. Error was: %s" % (to_native(module.params["name"]), to_native(e))
        )

    return result


def _start(module, sdk, instance_id):
    result = {}

    service = sdk.client(InstanceServiceStub)
    try:
        service_return = service.Start(StartInstanceRequest(instance_id=instance_id))
        result = MessageToDict(service_return)
    except Exception as e:
        module.fail_json(
            msg="unknown error starting instance by id %r. Error was: %s" % (to_native(instance_id), to_native(e))
        )

    return result


def _restart(module, sdk, instance_id):
    result = {}

    service = sdk.client(InstanceServiceStub)
    try:
        service_return = service.Restart(RestartInstanceRequest(instance_id=instance_id))
        result = MessageToDict(service_return)
    except Exception as e:
        module.fail_json(
            msg="unknown error restarting instance by id %r. Error was: %s" % (to_native(instance_id), to_native(e))
        )

    return result


def _stop(module, sdk, instance_id):
    result = {}

    service = sdk.client(InstanceServiceStub)
    try:
        service_return = service.Stop(StopInstanceRequest(instance_id=instance_id))
        result = MessageToDict(service_return)
    except Exception as e:
        module.fail_json(
            msg="unknown error stopping instance by id %r. Error was: %s" % (to_native(instance_id), to_native(e))
        )

    return result


def _delete(module, sdk, instance_id):
    result = {}

    service = sdk.client(InstanceServiceStub)
    try:
        service_return = service.Delete(DeleteInstanceRequest(instance_id=instance_id))
        result = MessageToDict(service_return)
    except Exception as e:
        module.fail_json(
            msg="unknown error deleting instance by id %r. Error was: %s" % (to_native(instance_id), to_native(e))
        )

    return result


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
                    type=dict(type="str", choices=["network-hdd", "network-ssd"]),
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
        required_one_of=[["iam_token", "token", "service_account_key"]],
        supports_check_mode=False,
    )

    sdk = yandexcloud.SDK(
        interceptor=yandexcloud.RetryInterceptor(max_retry_count=3, retriable_codes=[grpc.StatusCode.UNAVAILABLE]),
        iam_token=module.params["iam_token"],
        token=module.params["token"],
        service_account_key=module.params["service_account_key"]
    )

    instance = _find(module, sdk)

    match module.params["state"]:
        case "present":
            if instance == {}:
                _create(module, sdk)

                while (_find(module, sdk) == {}):
                    time.sleep(1)

                instance = _find(module, sdk)
                while not (_get(module, sdk, instance["id"])["status"] == "RUNNING"):
                    time.sleep(1)

                module.exit_json(
                    changed=True,
                    msg="instance %r created and running" % (to_native(module.params["name"])),
                    instance=_get(module, sdk, instance["id"])
                )

            elif instance["status"] == "STOPPED":
                _start(module, sdk, instance["id"])
                while not (_get(module, sdk, instance["id"])["status"] == "RUNNING"):
                    time.sleep(1)

                module.exit_json(
                    changed=True,
                    msg="instance %r exists and running" % (to_native(module.params["name"])),
                    instance=_get(module, sdk, instance["id"])
                )

            else:
                module.exit_json(
                    changed=False,
                    msg="instance %r exists and running" % (to_native(module.params["name"])),
                    instance=instance
                )

        case "restarted":
            if instance == {}:
                module.fail_json(
                    msg="not found instance with name %r" % (to_native(module.params["name"]))
                )

            elif instance["status"] == "STOPPED":
                _start(module, sdk, instance["id"])

            else:
                _restart(module, sdk, instance["id"])
                while not (_get(module, sdk, instance["id"])["status"] == "RESTARTING"):
                    time.sleep(1)

            while not (_get(module, sdk, instance["id"])["status"] == "RUNNING"):
                time.sleep(1)

            module.exit_json(
                changed=True,
                msg="instance %r restarted" % (to_native(module.params["name"])),
                instance=_get(module, sdk, instance["id"])
            )

        case "stopped":
            if instance == {}:
                module.fail_json(
                    msg="not found instance with name %r" % (to_native(module.params["name"]))
                )

            elif instance["status"] != "STOPPED":
                _stop(module, sdk, instance["id"])
                while not (_get(module, sdk, instance["id"])["status"] == "STOPPED"):
                    time.sleep(1)

            module.exit_json(
                changed=True,
                msg="instance %r stopped" % (to_native(module.params["name"])),
                instance=_get(module, sdk, instance["id"])
            )

        case "absent":
            if instance == {}:
                module.exit_json(
                    changed=False,
                    msg="not found instance with name %r" % (to_native(module.params["name"]))
                )

            else:
                _delete(module, sdk, instance["id"])
                while not (_find(module, sdk) == {}):
                    time.sleep(1)

                module.exit_json(
                    changed=True,
                    msg="instance %r deleted" % (to_native(module.params["name"])),
                )


if __name__ == "__main__":
    main()
