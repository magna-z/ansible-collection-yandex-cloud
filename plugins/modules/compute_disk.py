from __future__ import (absolute_import, division, print_function)
__metaclass__ = type

DOCUMENTATION = """
  module: compute_disk
  version_added: 0.1.0
  author: Maxim Zalysin <zalysin.m@gmail.com>
  short_description: Manage Yandex Cloud compute disk.
  description:
    - Module for managing compute disk resources.
  requirements:
    - python >= 3.10
    - yandexcloud >= 0.250.0
  notes:
    - 'API Reference: U(https://cloud.yandex.ru/en/docs/compute/api-ref/grpc/disk_service)'.
    - The I(iam_token), I(service_account_key) and I(token) options are mutually exclusive.  
    - The I(image_id) and I(snapshot_id) options are mutually exclusive.  
  options:
    state:
      type: str
      default: present
      choices:
        - present
        - absent
      description:
        - State of disk resources.
    folder_id:
      type: str
      required: true
      description:
        - ID of the folder to create a disk in.
          The maximum string length in characters is 50.
    name:
      type: str
      required: true
      description:
        - Name of the disk.
          Value must match the regular expression C([a-z]([-a-z0-9]{0,61}[a-z0-9])?).
    description:
      type: str
      description:
        - Description of the disk.
          The maximum string length in characters is 256.
    labels:
      type: dict
      description:
        - Resource labels as C(key:value) pairs. No more than 64 per resource.
        - The string length in characters for each key must be 1-63.
          Each key must match the regular expression C([a-z][-_./\\@0-9a-z]*). 
        - The maximum string length in characters for each value is 63.
          Each value must match the regular expression C([-_./\\@0-9a-z]*).
    type_id:
      type: str
      choices:
        - network-hdd
        - network-ssd
        - network-ssd-io-m3
        - network-ssd-nonreplicated
      description:
        - Required when C(state='present').
        - ID of the disk type.
          The maximum string length in characters is 50.
    zone_id:
      type: str
      description:
        - Required when C(state='present').
        - ID of the availability zone where the disk resides.
          The maximum string length in characters is 50.
    size:
      type: int
      description:
        - Required when C(state='present').
        - Size of the disk, specified in bytes.
          If the disk was created from a image, this value should be more than
          the P(yandex.cloud.compute_images)[*].min_disk_size value.
          Acceptable values are 4194304 to 28587302322176, inclusive.
        - For C(type_id=network-ssd-io-m3) and C(type_id=network-ssd-nonreplicated)
          disk size must be multiple of 99857989632.
    image_id:
      type: str
      description:
        - ID of the image to create the disk from.
          The maximum string length in characters is 50.
    snapshot_id:
      type: str
      description:
        - ID of the snapshot to restore the disk from.
          The maximum string length in characters is 50.
    block_size:
      type: int
      default: 4096
      choices:
        - 4096
        - 8192
        - 16384
        - 32768
        - 65536
        - 131072
      description:
        - Block size used for disk, specified in bytes.
    iam_token:
      type: str
      description:
        - An IAM token is a unique sequence of characters issued to a user after authentication.
        - The following regular expression describes a token: C(t1\.[A-Z0-9a-z_-]+[=]{0,2}\.[A-Z0-9a-z_-]{86}[=]{0,2})
    service_account_key:
      type: dict
      description:
        - A Service Account Key.
      suboptions:
        id:
          type: str
          description:
            - Key object ID
            - "id" field from service account key JSON
        service_account_id:
          type: str
          description:
            - Service account ID
            - "service_account_id" field from service account key JSON
        private_key:
          type: str
          description:
            - Private key
            - "private_key" field from service account key JSON
    token:
      type: str
      description:
        - An OAuth Token.
"""

EXAMPLES = """
- yandex.cloud.compute_disk:
   iam_token: t1.abcdefghij-123456789...
   folder_id: abcdefghijk123456789
   name: server-01-data
   description: server data disk
   labels:
     image-name: debian-11-v20240101
   zone_id: ru-central1-a
   type_id: network-ssd
   size: "{{ '20G' | ansible.builtin.human_to_bytes }}"
   image_id: abcdefghijk123456789
   block_size: "{{ '8K' | ansible.builtin.human_to_bytes }}"
 register: compute_disk
"""

RETURN = """
disk:
  returned: success
  type: complex
  description:
    - Dictionary with disk parameters.
  contains:
    block_size:
      returned: success
      type: str
      description:
        - Block size of the disk, specified in bytes.
    created_at:
      returned: success
      type: str
      description:
        - Disk creation date and time in ISO 8601 format in UTC timezone.
    description:
      returned: success
      type: str
      description:
        - Description of the disk. 0-256 characters long.
    disk_placement_policy:
      returned: success
      type: complex
      description:
        - Placement policy configuration.
      contains:
        placement_group_id:
          returned: success
          type: str
          description:
            - Placement group ID.
        placement_group_partition:
          returned: success
          type: str
          description:
            - Placement group partition number.
    folder_id:
      returned: success
      type: str
      description:
        - ID of the folder that the disk belongs to.
    id:
      returned: success
      type: str
      description:
        - ID of the disk.
    instance_ids:
      returned: success
      type: list
      description:
        - Array of instances to which the disk is attached.
    labels:
      returned: success
      type: dict
      description:
        - Resource labels as key:value pairs. Maximum of 64 per resource.
    name:
      returned: success
      type: str
      description:
        - Name of the disk. 1-63 characters long.
    product_ids:
      returned: success
      type: list
      description:
        - License IDs that indicate which licenses are attached to this resource.
          License IDs are used to calculate additional charges for the use of the virtual machine.
        - The correct license ID is generated by the platform.
          IDs are inherited by new resources created from this resource.
        - If you know the license IDs, specify them when you create the image.
          For example, if you create a disk image using a third-party utility and load it into Object Storage,
          the license IDs will be lost. 
    size:
      returned: success
      type: str
      description:
        - Size of the disk, specified in bytes.
    source_image_id:
      returned: success
      type: str
      description:
        - ID of the image that was used for disk creation.
    source_snapshot_id:
      returned: success
      type: str
      description:
        - ID of the snapshot that was used for disk creation.
    status:
      returned: success
      type: str
      description:
        - Current status of the disk.
          C(CREATING): Disk is being created.
          C(READY): Disk is ready to use.
          C(ERROR): Disk encountered a problem and cannot operate.
          C(DELETING): Disk is being deleted.
    type_id:
      returned: success
      type: str
      description:
        - ID of the disk type.
    zone_id:
      returned: success
      type: str
      description:
        - ID of the availability zone where the disk resides.
diff:
  returned: success
  type: str
  description:
    - 
"""

from difflib import ndiff
from json import dumps
from time import sleep

from google.protobuf.field_mask_pb2 import FieldMask

from yandex.cloud.operation.operation_service_pb2_grpc import OperationServiceStub
from yandex.cloud.operation.operation_service_pb2 import GetOperationRequest
from yandex.cloud.compute.v1.disk_service_pb2_grpc import DiskServiceStub
from yandex.cloud.compute.v1.disk_service_pb2 import (
    CreateDiskRequest,
    DeleteDiskRequest,
    GetDiskRequest,
    ListDisksRequest,
    UpdateDiskRequest,
)

from ansible.module_utils.basic import AnsibleModule
from ansible.module_utils.common.text.converters import to_native
from ansible.module_utils.common.yaml import *

from ..module_utils.common import (OperationError, message_to_dict)
from ..module_utils.sdk import client


def _find(module, service):
    disk = dict()

    request = ListDisksRequest(
        folder_id=module.params['folder_id'],
        filter="name = %r" % module.params['name'],
        page_size=1,
    )

    try:
        response = message_to_dict(service.List(request))
        if len(response['disks']) == 1:
            disk = response['disks'][0]

    except Exception as e:
        module.fail_json(
            msg="unknown error find disk %r. Error was: %s" % (to_native(module.params['name']), to_native(e)),
        )

    return disk


def _get(module, service, disk_id):
    disk = dict()

    request = GetDiskRequest(disk_id=disk_id)

    try:
        disk = message_to_dict(service.Get(request))

    except Exception as e:
        module.fail_json(
            msg="unknown error get disk %r. Error was: %s" % (to_native(module.params['name']), to_native(e)),
        )

    return disk


def _create(module, service):
    operation = dict()

    request = CreateDiskRequest(
        folder_id=module.params['folder_id'],
        name=module.params['name'],
        description=module.params['description'],
        labels=module.params['labels'],
        type_id=module.params['type_id'],
        zone_id=module.params['zone_id'],
        size=module.params['size'],
        image_id=module.params['image_id'],
        snapshot_id=module.params['snapshot_id'],
        block_size=module.params['block_size'],
    )

    try:
        operation = message_to_dict(service.Create(request))

    except Exception as e:
        module.fail_json(
            msg="unknown error create disk %r. Error was: %s" % (to_native(module.params['name']), to_native(e)),
        )

    return operation


def _update(module, service, disk_id):
    operation = dict()

    request = UpdateDiskRequest(
        disk_id=disk_id,
        update_mask=FieldMask(paths=['size', 'description', 'labels']),
        size=module.params['size'],
        description=module.params['description'],
        labels=module.params['labels'],
    )

    try:
        operation = message_to_dict(service.Update(request))

    except Exception as e:
        module.fail_json(
            msg="unknown error update disk %r. Error was: %s" % (to_native(module.params['name']), to_native(e)),
        )

    return operation


def _delete(module, service, disk_id):
    operation = dict()

    request = DeleteDiskRequest(
        disk_id=disk_id
    )

    try:
        operation = message_to_dict(service.Delete(request))

    except Exception as e:
        module.fail_json(
            msg="unknown error delete disk %r. Error was: %s" % (to_native(module.params['name']), to_native(e)),
        )

    return operation


def _wait(module, service, operation_id):
    request = GetOperationRequest(operation_id=operation_id)

    try:
        while True:
            sleep(1)
            operation = message_to_dict(service.Get(request))
            if 'done' in operation and operation['done']:
                if 'error' in operation:
                    raise OperationError(
                        "unknown operation error code %r. Error was: %s" %
                        (to_native(operation['error']['code']), to_native(operation['error']['message']))
                    )
                break
    except Exception as e:
        module.fail_json(
            msg="unknown error operation disk %r. Error was: %s" % (to_native(module.params['name']), to_native(e)),
        )


def main():
    module = AnsibleModule(
        argument_spec=dict(
            state=dict(type='str', default='present', choices=['present', 'absent']),
            folder_id=dict(type='str', required=True),
            name=dict(type='str', required=True),
            description=dict(type='str', default=''),
            labels=dict(type='dict', default=dict()),
            type_id=dict(
                type='str',
                choices=['network-hdd', 'network-ssd', 'network-ssd-io-m3', 'network-ssd-nonreplicated'],
            ),
            zone_id=dict(type='str'),
            size=dict(type='int'),
            image_id=dict(type='str'),
            snapshot_id=dict(type='str'),
            block_size=dict(type='int', default=4096, choices=[4096, 8192, 16384, 32768, 65536, 131072]),
            # disk_placement_policy=dict(),
            # snapshot_schedule_ids=dict(type='list'),
            iam_token=dict(type='str', no_log=True),
            service_account_key=dict(type='dict', no_log=True),
            token=dict(type='str', no_log=True),
        ),
        required_one_of=[('iam_token', 'service_account_key', 'token')],
        required_if=[
            ('state', 'present', ('type_id', 'zone_id', 'size'), False),
        ],
        mutually_exclusive=[('iam_token', 'service_account_key', 'token'), ['image_id', 'snapshot_id']],
        supports_check_mode=False,
    )

    disk_service = client(
        service=DiskServiceStub,
        iam_token=module.params['iam_token'],
        token=module.params['token'],
        service_account_key=module.params['service_account_key'],
    )

    operation_service = client(
        service=OperationServiceStub,
        iam_token=module.params['iam_token'],
        token=module.params['token'],
        service_account_key=module.params['service_account_key'],
    )

    disk = _find(module, disk_service)

    match module.params['state']:
        case 'present':
            if disk == {}:
                operation = _create(module, disk_service)
                _wait(module, operation_service, operation['id'])

                module.exit_json(
                    changed=True,
                    msg="disk %r created" % (to_native(module.params['name'])),
                    disk=_get(module, disk_service, operation['metadata']['disk_id']),
                )

            elif (
                str(disk['size']) != str(module.params['size'])
                or str(disk['description']) != str(module.params['description'])
                or dict(sorted(disk['labels'].items())) != dict(sorted(module.params['labels'].items()))
            ):
                operation = _update(module, disk_service, disk['id'])
                _wait(module, operation_service, operation['id'])

                diff = ndiff(
                    dumps({
                        'size': str(disk['size']),
                        'description': str(disk['description']),
                        'labels': dict(sorted(disk['labels'].items())),
                    }, indent=2, sort_keys=True).splitlines(keepends=True),
                    dumps({
                        'size': str(module.params['size']),
                        'description': str(module.params['description']),
                        'labels': dict(sorted(module.params['labels'].items())),

                    }, indent=2, sort_keys=True).splitlines(keepends=True),
                )

                module.exit_json(
                    changed=True,
                    msg="disk %r updated" % (to_native(module.params['name'])),
                    disk=_get(module, disk_service, disk['id']),
                    diff=''.join(diff),
                )

            else:
                module.exit_json(
                    changed=False,
                    msg="disk %r exists and ready" % (to_native(module.params["name"])),
                    disk=disk,
                )

        case 'absent':
            if disk == {}:
                module.exit_json(
                    changed=False,
                    msg="disk %r not exists" % (to_native(module.params['name'])),
                )

            else:
                operation = _delete(module, disk_service, disk['id'])
                _wait(module, operation_service, operation['id'])

                module.exit_json(
                    changed=True,
                    msg="disk %r deleted" % (to_native(module.params['name'])),
                )


if __name__ == '__main__':
    main()
