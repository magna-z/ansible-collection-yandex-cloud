from __future__ import (absolute_import, division, print_function)
__metaclass__ = type

DOCUMENTATION = """
  module: compute_instance
  version_added: 0.1.0
  author: Maxim Zalysin <zalysin.m@gmail.com>
  short_description: Manage Yandex Cloud compute instance.
  description:
    - Module for managing compute instance resources.
  requirements:
    - python >= 3.10
    - yandexcloud >= 0.250.0
  notes:
    - 'API Reference: U(https://cloud.yandex.ru/en/docs/compute/api-ref/grpc/instance_service)'.
    - The I(iam_token), I(service_account_key) and I(token) options are mutually exclusive.  
    - 
  options:
    state:
      type: str
      default: present
      choices:
        - present
        - restarted
        - stopped
        - absent
      description:
        - State of instance resources.
    folder_id:
      type: str
      required: true
      description:
        - ID of the folder to create a instance in.
          The maximum string length in characters is 50.
    name:
      type: str
      required: true
      description:
        - Name of the instance.
          Value must match the regular expression C([a-z]([-a-z0-9]{0,61}[a-z0-9])?).
    description:
      type: str
      description:
        - Description of the instance.
          The maximum string length in characters is 256.
    labels:
      type: dict
      description:
        - Resource labels as C(key:value) pairs. No more than 64 per resource.
        - The string length in characters for each key must be 1-63.
          Each key must match the regular expression C([a-z][-_./\\@0-9a-z]*). 
        - The maximum string length in characters for each value is 63.
          Each value must match the regular expression C([-_./\\@0-9a-z]*).
    zone_id:
      type: str
      description:
        - Required when C(state='present').
        - ID of the availability zone where the instance resides.
          The maximum string length in characters is 50.
    platform_id:
      type: str
      default: standard-v3
      choices:
        - standard-v1
        - standard-v2
        - standard-v3
        - highfreq-v3
        - gpu-standard-v1
        - gpu-standard-v2
        - gpu-standard-v3
        - standard-v3-t4
      description:
        - ID of the hardware platform configuration for the instance.
          This field affects the available values in resources_spec field.
        - Platforms allows you to create various types of instances:
          with a large amount of memory, with a large number of cores, with a burstable performance.
    resources:
      type: dict
      suboptions:
        memory:
          type: int
          required: true
          description:
            - The amount of memory available to the instance, specified in bytes.
              The maximum value is 274877906944.
        cores:
          type: int
          required: true
          description:
            - The number of cores available to the instance.
              Value must be equal to 2,4,6,8,10,12,14,16,18,20,22,24,26,28,30,32,34,36,40,44,48,52,56,60,64,68,72,76,80.
        core_fraction:
          type: int
          default: 100
          description:
            - Baseline level of CPU performance with the ability to burst performance above that baseline level.
              This field sets baseline performance for each core.
            - For example, if you need only 5% of the CPU performance, you can set C(core_fraction=5).
              Value must be equal to 0,5,20,50,100.
        gpus:
          type: int
          default: 0
          description:
            - The number of GPUs available to the instance.
              Value must be equal to 0,1,2,4.
      description:
        - Computing resources of the instance, such as the amount of memory and number of cores.
    metadata:
      type: dict
      description:
        - The metadata C(key:value) pairs that will be assigned to this instance.
          This includes custom metadata and predefined keys.
          The total size of all keys and values must be less than 512 KB.
        - Values are free-form strings, and only have meaning as interpreted by the programs which configure the instance.
          The values must be 256 KB or less.
        - For example, you may use the metadata in order to provide your public SSH key to the instance. 
    metadata_options:
      type: dict
      suboptions:
        aws_v1_http_endpoint:
          type: bool
          default: true
          description:
            - Enabled access to AWS flavored metadata (IMDSv1).
        aws_v1_http_token:
          type: bool
          default: false
          description:
            - Enabled access to IAM credentials with AWS flavored metadata (IMDSv1).
        gce_http_endpoint:
          type: bool
          default: true
          description:
            - Enabled access to GCE flavored metadata.
        gce_http_token:
          type: bool
          default: true
          description:
            - Enabled access to IAM credentials with GCE flavored metadata.
      description:
        - Options allow user to configure access to instance's metadata.
    boot_disk:
      type: dict
      suboptions:
        mode:
          type: str
          default: READ_WRITE
          choices
            - READ_ONLY
            - READ_WRITE
          description:
            - The mode in which to attach this disk.
              C(READ_ONLY): Read-only access.
              C(READ_WRITE): Read/Write access.
        device_name:
          type: str
          description:
            - Specifies a unique serial number of your choice that is reflected into the /dev/disk/by-id/ tree
              of a Linux operating system running within the instance.
            - This value can be used to reference the device for mounting, resizing, and so on, from within the instance.
              If not specified, a random value will be generated.
              Value must match the regular expression C([a-z][a-z0-9-_]{,19}).
        auto_delete:
          type: bool
          description:
            - Specifies whether the disk will be auto-deleted when the instance is deleted.
        disk_id:
          type: str
          required: true
          description:
            - ID of the disk that should be attached.
              The maximum string length in characters is 50.
      description:
        - Boot disk to attach to the instance.
    secondary_disks:
      type: list
      elements: dict
      suboptions:
        mode:
          type: str
          default: READ_WRITE
          choices
            - READ_ONLY
            - READ_WRITE
          description:
            - The mode in which to attach this disk.
              C(READ_ONLY): Read-only access.
              C(READ_WRITE): Read/Write access.
        device_name:
          type: str
          description:
            - Specifies a unique serial number of your choice that is reflected into the /dev/disk/by-id/ tree
              of a Linux operating system running within the instance.
            - This value can be used to reference the device for mounting, resizing, and so on, from within the instance.
              If not specified, a random value will be generated.
              Value must match the regular expression C([a-z][a-z0-9-_]{,19}).
        auto_delete:
          type: bool
          description:
            - Specifies whether the disk will be auto-deleted when the instance is deleted.
        disk_id:
          type: str
          required: true
          description:
            - ID of the disk that should be attached.
              The maximum string length in characters is 50.
      description:
        - Array of secondary disks to attach to the instance.
          The maximum number of elements is 3.
    local_discs:
      description:
        - Array of local disks to attach to the instance.
    filesystems:
      description:
        - Array of filesystems to attach to the instance.
        - The filesystems must reside in the same availability zone as the instance.
        - To use the instance with an attached filesystem, the latter must be mounted.
    network_interfaces:
      type: list
      elements: dict
      suboptions:
        subnet_id:
          type: str
          required: true
          description:
            - ID of the subnet.
              The maximum string length in characters is 50.
        primary_v4_address:
          type: dict
          suboptions:
            address:
              type: str
              description:
                - An IPv4 internal network address that is assigned to the instance for this network interface.
                  If not specified by the user, an unused internal IP is assigned by the system.
            one_to_one_nat:
              type: dict
              suboptions:
                ip_version:
                  type: string
                  default: IPV4
                  choices
                    - IPV4
                    - IPV6
                  description:
                    - External IP address version.
                      C(IPV4): IPv4 address, for example 192.0.2.235.
                      C(IPV6): IPv6 address. Not available yet.
                address:
                  type: str
                  description:
                    - 
                dns_records:
                  type: list
                  elements: dict
                  suboptions:
                    fqdn:
                      type: str
                      required: true
                      description:
                        - Fully qualified domain name.
                    dns_zone_id:
                      type: str
                      description:
                        - DNS zone id.
                          If not set, private zone used.
                    ttl:
                      type: int
                      description:
                        - DNS record TTL, values in 0-86400.
                    ptr:
                      type: bool
                      description:
                        - When set to true, also create PTR DNS record.
                  description:
                    - Internal DNS configuration.
              description:
                - An external IP address configuration.
                  If not specified, then this instance will have no external internet access.
            dns_records:
              type: list
              elements: dict
              suboptions:
                fqdn:
                  type: str
                  required: true
                  description:
                    - Fully qualified domain name.
                dns_zone_id:
                  type: str
                  description:
                    - DNS zone id.
                      If not set, private zone used.
                ttl:
                  type: int
                  description:
                    - DNS record TTL, values in 0-86400.
                ptr:
                  type: bool
                  description:
                    - When set to true, also create PTR DNS record.
              description:
                - Internal DNS configuration.
          description:
            - Primary IPv4 address that will be assigned to the instance for this network interface.
        primary_v6_address:
          type: dict
          suboptions:
            address:
              type: str
              description:
                - An IPv6 internal network address that is assigned to the instance for this network interface.
                  If not specified by the user, an unused internal IP is assigned by the system.
              suboptions:
                ip_version:
                  type: string
                  default: IPV4
                  choices
                    - IPV4
                    - IPV6
                  description:
                    - External IP address version.
                      C(IPV4): IPv4 address, for example 192.0.2.235.
                      C(IPV6): IPv6 address. Not available yet.
                address:
                  type: str
                  description:
                    - 
                dns_records:
                  type: list
                  elements: dict
                  suboptions:
                    fqdn:
                      type: str
                      required: true
                      description:
                        - Fully qualified domain name.
                    dns_zone_id:
                      type: str
                      description:
                        - DNS zone id.
                          If not set, private zone used.
                    ttl:
                      type: int
                      description:
                        - DNS record TTL, values in 0-86400.
                    ptr:
                      type: bool
                      description:
                        - When set to true, also create PTR DNS record.
                  description:
                    - Internal DNS configuration.
              description:
                - An external IP address configuration.
                  If not specified, then this instance will have no external internet access.
            dns_records:
              type: list
              elements: dict
              suboptions:
                fqdn:
                  type: str
                  required: true
                  description:
                    - Fully qualified domain name.
                dns_zone_id:
                  type: str
                  description:
                    - DNS zone id.
                      If not set, private zone used.
                ttl:
                  type: int
                  description:
                    - DNS record TTL, values in 0-86400.
                ptr:
                  type: bool
                  description:
                    - When set to true, also create PTR DNS record.
              description:
                - Internal DNS configuration.
          description:
            - Primary IPv6 address that will be assigned to the instance for this network interface.
            - IPv6 not available yet.
        security_group_ids:
          type: list
          elements: str
          description:
            - ID's of security groups attached to the interface.
      description:
        - Network configuration for the instance.
          Specifies how the network interface is configured to interact with other services on the internal network and on the internet.
          Currently only one network interface is supported per instance.
          The number of elements must be exactly 1.
    hostname:
      type: str
      description:
        - Host name for the instance.
        - The host name must be unique within the network and region.
          If not specified, the host name will be equal to ID of the instance and FQDN will be <id>.auto.internal.
        - Otherwise FQDN will be <hostname>.<region_id>.internal.
          Value must match the regular expression C(|[a-z]([-a-z0-9]{0,61}[a-z0-9])?).
    scheduling_policy:
      description:
        - Scheduling policy configuration.
    service_account_id:
      type: str
      description:
        - ID of the service account to use for authentication inside the instance.
    network_settings:
      type: dict
      suboptions:
        type:
          default: STANDARD
          choices:
            - STANDARD
            - SOFTWARE_ACCELERATED
            - HARDWARE_ACCELERATED
          description:
            - Network type.
              C(STANDARD): Standard network.
              C(SOFTWARE_ACCELERATED): Software accelerated network.
              C(HARDWARE_ACCELERATED): Hardware accelerated network (not available yet, reserved for future use).
      description:
        - Network settings.
    placement_policy:
      description:
        - Placement policy configuration.
    gpu_settings:
      type: dict
      suboptions:
        gpu_cluster_id:
          type: str
          description:
            - Attach instance to specified GPU cluster.
      description:
        - GPU settings.
    maintenance_policy:
      type: str
      choices:
        - MIGRATE
        - RESTART
      description:
        - Behaviour on maintenance events.
          C(RESTART): Restart instance to move it to another host during maintenance.
          C(MIGRATE): Use live migration to move instance to another host during maintenance.
    maintenance_grace_period:
      type: int
      description:
        - Seconds between notification via metadata service and maintenance.
          Acceptable values are 1 to 86400, inclusive.
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
- yandex.cloud.compute_instance:
    iam_token: t1.abcdefghij-123456789...
    folder_id: abcdefghijk123456789
    name: server-01
    hostname: server-01
    zone_id: ru-central1-a
    resources:
      cores: 2
      core_fraction: 100
      memory: "{{ '4G' | ansible.builtin.human_to_bytes }}"
    boot_disk:
      auto_delete: true
      disk_id: abcdefghijk123456789
    network_interfaces:
      - subnet_id: abcdefghijk123456789
        primary_v4_address: {}
    metadata:
      install-unified-agent: "0"
      ssh-keys: ansible:ecdsa-sha2-nistp256 ...
      user-data: |
        #cloud-config
        runcmd: []
        datasource:
         Ec2:
          strict_id: false
        ssh_pwauth: no
        users:
          - name: ansible
            sudo: ALL=(ALL) NOPASSWD:ALL
            shell: /bin/bash
            ssh_authorized_keys:
              - ecdsa-sha2-nistp256 ...
  register: compute_instance
"""

RETURN = """
instance:
  returned: success
  type: complex
  description:
    - Dictionary with instance parameters.
  contains:
    
diff:
  
"""

# from difflib import ndiff
# from json import dumps
from time import sleep

from google.protobuf.duration_pb2 import Duration
# from google.protobuf.field_mask_pb2 import FieldMask

from yandex.cloud.operation.operation_service_pb2_grpc import OperationServiceStub
from yandex.cloud.operation.operation_service_pb2 import GetOperationRequest
from yandex.cloud.compute.v1.instance_pb2 import (
    GpuSettings,
    MetadataOptions,
    NetworkSettings,
)
from yandex.cloud.compute.v1.instance_service_pb2_grpc import InstanceServiceStub
from yandex.cloud.compute.v1.instance_service_pb2 import (
    AttachedDiskSpec,
    CreateInstanceRequest,
    DeleteInstanceRequest,
    DnsRecordSpec,
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

from ..module_utils.common import (OperationError, bool_to_enum, message_to_dict)
from ..module_utils.sdk import client


def _find(module, service):
    instance = dict()

    folder_id = module.params['folder_id']
    filter = "name = %r" % module.params['name']
    request = ListInstancesRequest(folder_id=folder_id, filter=filter, order_by='name asc')

    try:
        response = message_to_dict(service.List(request))
        if len(response['instances']) == 1:
            instance = response['instances'][0]

    except Exception as e:
        module.fail_json(
            msg="unknown error find instance %r by filter %r. Error was: %s"
            % (to_native(folder_id), to_native(filter), to_native(e))
        )

    return instance


def _get(module, service, instance_id):
    instance = dict()

    request = GetInstanceRequest(instance_id=instance_id, view='FULL')

    try:
        instance = message_to_dict(service.Get(request))

    except Exception as e:
        module.fail_json(
            msg="unknown error getting instance by id %r. Error was: %s" % (to_native(instance_id), to_native(e))
        )

    return instance


def _create(module, service):
    operation = dict()

    secondary_disk_specs = list()
    for secondary_disk in module.params['secondary_disks']:
        secondary_disk_specs.append(
            AttachedDiskSpec(
                mode=secondary_disk['mode'],
                device_name=secondary_disk['device_name'],
                auto_delete=secondary_disk['auto_delete'],
                disk_id=secondary_disk['disk_id'],
            ),
        )

    network_interface_specs = list()
    for network_interface in module.params['network_interfaces']:
        network_interface_specs.append(
            NetworkInterfaceSpec(
                subnet_id=network_interface['subnet_id'],
                primary_v4_address_spec=PrimaryAddressSpec(
                    address=network_interface['primary_v4_address']['address'],
                    one_to_one_nat_spec=OneToOneNatSpec(
                        ip_version=network_interface['primary_v4_address']['one_to_one_nat']['ip_version'],
                        address=network_interface['primary_v4_address']['one_to_one_nat']['address'],
                        dns_record_specs=list(
                            DnsRecordSpec(
                                fqdn=dns_record['fqdn'],
                                dns_zone_id=dns_record['dns_zone_id'],
                                ttl=dns_record['ttl'],
                                ptr=dns_record['ptr'],
                            ) for dns_record in network_interface['primary_v4_address']['one_to_one_nat']['dns_records']
                        ) if network_interface['primary_v4_address']['one_to_one_nat']['dns_records'] else None
                    ) if network_interface['primary_v4_address']['one_to_one_nat'] else None,
                    dns_record_specs=list(
                        DnsRecordSpec(
                            fqdn=dns_record['fqdn'],
                            dns_zone_id=dns_record['dns_zone_id'],
                            ttl=dns_record['ttl'],
                            ptr=dns_record['ptr'],
                        ) for dns_record in network_interface['primary_v4_address']['dns_records']
                    ) if network_interface['primary_v4_address']['dns_records'] else None
                ) if network_interface['primary_v4_address'] else None,
                primary_v6_address_spec=PrimaryAddressSpec(
                    address=network_interface['primary_v6_address']['address'],
                    one_to_one_nat_spec=OneToOneNatSpec(
                        ip_version=network_interface['primary_v6_address']['one_to_one_nat']['ip_version'],
                        address=network_interface['primary_v6_address']['one_to_one_nat']['address'],
                        dns_record_specs=list(
                            DnsRecordSpec(
                                fqdn=dns_record['fqdn'],
                                dns_zone_id=dns_record['dns_zone_id'],
                                ttl=dns_record['ttl'],
                                ptr=dns_record['ptr'],
                            ) for dns_record in network_interface['primary_v6_address']['one_to_one_nat']['dns_records']
                        ) if network_interface['primary_v6_address']['one_to_one_nat']['dns_records'] else None
                    ) if network_interface['primary_v6_address']['one_to_one_nat'] else None,
                    dns_record_specs=list(
                        DnsRecordSpec(
                            fqdn=dns_record['fqdn'],
                            dns_zone_id=dns_record['dns_zone_id'],
                            ttl=dns_record['ttl'],
                            ptr=dns_record['ptr'],
                        ) for dns_record in network_interface['primary_v6_address']['dns_records']
                    ) if network_interface['primary_v6_address']['dns_records'] else None
                ) if network_interface['primary_v6_address'] else None,
                security_group_ids=network_interface['security_group_ids']
            )
        )

    request = CreateInstanceRequest(
        folder_id=module.params['folder_id'],
        name=module.params['name'],
        description=module.params['description'],
        labels=module.params['labels'],
        zone_id=module.params['zone_id'],
        platform_id=module.params['platform_id'],
        resources_spec=ResourcesSpec(
            memory=module.params['resources']['memory'],
            gpus=module.params['resources']['gpus'],
            cores=module.params['resources']['cores'],
            core_fraction=module.params['resources']['core_fraction'],
        ),
        metadata=module.params['metadata'],
        metadata_options=MetadataOptions(
            aws_v1_http_endpoint=bool_to_enum(module.params['metadata_options']['aws_v1_http_endpoint']),
            aws_v1_http_token=bool_to_enum(module.params['metadata_options']['aws_v1_http_token']),
            gce_http_endpoint=bool_to_enum(module.params['metadata_options']['gce_http_endpoint']),
            gce_http_token=bool_to_enum(module.params['metadata_options']['gce_http_token']),
        ) if module.params['metadata_options'] else None,
        boot_disk_spec=AttachedDiskSpec(
            mode=module.params['boot_disk']['mode'],
            device_name=module.params['boot_disk']['device_name'],
            auto_delete=module.params['boot_disk']['auto_delete'],
            disk_id=module.params['boot_disk']['disk_id'],
        ),
        secondary_disk_specs=secondary_disk_specs,
        # local_disk_specs=,
        # filesystem_specs=,
        network_interface_specs=network_interface_specs,
        hostname=module.params['hostname'],
        # scheduling_policy=,
        service_account_id=module.params['service_account_id'],
        network_settings=NetworkSettings(
            type=module.params['network_settings']['type'],
        ) if module.params['network_settings'] else None,
        # placement_policy=,
        gpu_settings=GpuSettings(
            gpu_cluster_id=module.params['gpu_settings']['gpu_cluster_id'],
        ) if module.params['gpu_settings'] else None,
        maintenance_policy=module.params['maintenance_policy'],
        maintenance_grace_period=Duration(seconds=module.params['maintenance_grace_period']),
    )

    try:
        operation = message_to_dict(service.Create(request))

    except Exception as e:
        module.fail_json(
            msg="unknown error create instance %r. Error was: %s" % (to_native(module.params['name']), to_native(e))
        )

    return operation


# def _update(module, service):
#     operation = dict()
#
#     return operation


def _start(module, service, instance_id):
    operation = dict()

    request = StartInstanceRequest(instance_id=instance_id)

    try:
        operation = message_to_dict(service.Start(request))

    except Exception as e:
        module.fail_json(
            msg="unknown error starting instance by id %r. Error was: %s" % (to_native(instance_id), to_native(e))
        )

    return operation


def _restart(module, service, instance_id):
    operation = dict()

    request = RestartInstanceRequest(instance_id=instance_id)

    try:
        operation = message_to_dict(service.Restart(request))

    except Exception as e:
        module.fail_json(
            msg="unknown error restarting instance by id %r. Error was: %s" % (to_native(instance_id), to_native(e))
        )

    return operation


def _stop(module, service, instance_id):
    operation = dict()

    request = StopInstanceRequest(instance_id=instance_id)

    try:
        operation = message_to_dict(service.Stop(request))

    except Exception as e:
        module.fail_json(
            msg="unknown error stopping instance by id %r. Error was: %s" % (to_native(instance_id), to_native(e))
        )

    return operation


def _delete(module, service, instance_id):
    operation = dict()

    request = DeleteInstanceRequest(instance_id=instance_id)

    try:
        operation = message_to_dict(service.Delete(request))

    except Exception as e:
        module.fail_json(
            msg="unknown error deleting instance by id %r. Error was: %s" % (to_native(instance_id), to_native(e))
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
    dns_record_params = dict(
        type='list',
        elements='dict',
        default=list(),
        options=dict(
            fqdn=dict(type='str', required=True),
            dns_zone_id=dict(type='str'),
            ttl=dict(type='int'),
            ptr=dict(type='bool'),
        ),
    )

    primary_address_params = dict(
        type='dict',
        options=dict(
            address=dict(type='str'),
            one_to_one_nat=dict(
                type='dict',
                options=dict(
                    ip_version=dict(type='string', default='IPV4', choices=['IPV4', 'IPV6']),
                    address=dict(type='str'),
                    dns_records=dns_record_params,
                ),
            ),
            dns_records=dns_record_params,
        ),
    )

    module = AnsibleModule(
        argument_spec=dict(
            state=dict(type='str', default='present', choices=['present', 'restarted', 'stopped', 'absent']),
            folder_id=dict(type='str', required=True),
            name=dict(type='str', required=True),
            description=dict(type='str'),
            labels=dict(type='dict'),
            zone_id=dict(type='str'),
            platform_id=dict(
                type='str',
                default='standard-v3',
                choices=[
                    'standard-v1', 'standard-v2', 'standard-v3',
                    'highfreq-v3',
                    'gpu-standard-v1', 'gpu-standard-v2', 'gpu-standard-v3',
                    'standard-v3-t4',
                ],
            ),
            resources=dict(
                type='dict',
                options=dict(
                    memory=dict(type='int', required=True),
                    cores=dict(type='int', required=True),
                    core_fraction=dict(type='int', default=100),
                    gpus=dict(type='int', default=0),
                ),
            ),
            metadata=dict(type='dict'),
            metadata_options=dict(
                type='dict',
                options=dict(
                    aws_v1_http_endpoint=dict(type='bool', default=True),
                    aws_v1_http_token=dict(type='bool', default=False),
                    gce_http_endpoint=dict(type='bool', default=True),
                    gce_http_token=dict(type='bool', default=True),
                ),
            ),
            boot_disk=dict(
                type='dict',
                options=dict(
                    mode=dict(type='str', default='READ_WRITE', choices=['READ_ONLY', 'READ_WRITE']),
                    device_name=dict(type='str'),
                    auto_delete=dict(type='bool'),
                    disk_id=dict(type='str', required=True),
                ),
            ),
            secondary_disks=dict(
                type='list',
                elements='dict',
                default=list(),
                options=dict(
                    mode=dict(type='str', default='READ_WRITE', choices=['READ_ONLY', 'READ_WRITE']),
                    device_name=dict(type='str'),
                    auto_delete=dict(type='bool'),
                    disk_id=dict(type='str', required=True),
                ),
            ),
            # local_discs=dict(),
            # filesystems=dict(),
            network_interfaces=dict(
                type='list',
                elements='dict',
                options=dict(
                    subnet_id=dict(type='str', required=True),
                    primary_v4_address=primary_address_params,
                    primary_v6_address=primary_address_params,
                    security_group_ids=dict(type='list', elements='str', default=list()),
                ),
            ),
            hostname=dict(type='str'),
            # scheduling_policy=dict(),
            service_account_id=dict(type='str'),
            network_settings=dict(
                type='dict',
                options=dict(
                    type=dict(
                        type='str',
                        default='STANDARD',
                        choices=['STANDARD', 'SOFTWARE_ACCELERATED', 'HARDWARE_ACCELERATED'],
                    ),
                ),
            ),
            # placement_policy=dict(),
            gpu_settings=dict(
                type='dict',
                options=dict(
                    gpu_cluster_id=dict(type='str'),
                ),
            ),
            maintenance_policy=dict(type='str', choices=['MIGRATE', 'RESTART']),
            maintenance_grace_period=dict(type='int'),
            iam_token=dict(type='str'),
            token=dict(type='str'),
            service_account_key=dict(type='dict'),
        ),
        required_one_of=[('iam_token', 'token', 'service_account_key')],
        required_if=[
            ('state', 'present', ('zone_id', 'platform_id', 'resources', 'boot_disk', 'network_interfaces'), False),
        ],
        mutually_exclusive=[('iam_token', 'service_account_key', 'token')],
        supports_check_mode=False,
    )

    instance_service = client(
        service=InstanceServiceStub,
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

    instance = _find(module, instance_service)

    match module.params['state']:
        case 'present':
            if instance == {}:
                operation = _create(module, instance_service)
                _wait(module, operation_service, operation['id'])

                module.exit_json(
                    changed=True,
                    msg="instance %r created and running" % (to_native(module.params['name'])),
                    instance=_get(module, instance_service, operation['metadata']['instance_id']),
                )

            elif instance['status'] == 'STOPPED':
                operation = _start(module, instance_service, instance['id'])
                _wait(module, operation_service, operation['id'])

                module.exit_json(
                    changed=True,
                    msg="instance %r exists and running" % (to_native(module.params['name'])),
                    instance=_get(module, instance_service, instance['id']),
                )

            else:
                module.exit_json(
                    changed=False,
                    msg="instance %r exists and running" % (to_native(module.params['name'])),
                    instance=instance,
                )

        case 'restarted':
            if instance == {}:
                module.fail_json(
                    msg="not found instance with name %r" % (to_native(module.params['name']))
                )

            elif instance['status'] == 'STOPPED':
                operation = _start(module, instance_service, instance['id'])
                _wait(module, operation_service, operation['id'])

            else:
                operation = _restart(module, instance_service, instance['id'])
                _wait(module, operation_service, operation['id'])

            module.exit_json(
                changed=True,
                msg="instance %r restarted" % (to_native(module.params['name'])),
                instance=_get(module, instance_service, instance['id']),
            )

        case 'stopped':
            if instance == {}:
                module.fail_json(
                    msg="not found instance with name %r" % (to_native(module.params['name']))
                )

            elif instance["status"] == 'STOPPED':
                module.exit_json(
                    changed=False,
                    msg="instance %r stopped" % (to_native(module.params['name'])),
                    instance=_get(module, instance_service, instance['id']),
                )

            else:
                operation = _stop(module, instance_service, instance['id'])
                _wait(module, operation_service, operation['id'])

            module.exit_json(
                changed=True,
                msg="instance %r stopped" % (to_native(module.params['name'])),
                instance=_get(module, instance_service, instance['id']),
            )

        case 'absent':
            if instance == {}:
                module.exit_json(
                    changed=False,
                    msg="not found instance with name %r" % (to_native(module.params['name'])),
                )

            else:
                operation = _delete(module, instance_service, instance['id'])
                _wait(module, operation_service, operation['id'])

                module.exit_json(
                    changed=True,
                    msg="instance %r deleted" % (to_native(module.params['name'])),
                )


if __name__ == '__main__':
    main()
