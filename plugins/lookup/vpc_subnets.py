from __future__ import (absolute_import, division, print_function)
__metaclass__ = type

DOCUMENTATION = """
  name: vpc_subnets
  author: Maxim Zalysin <zalysin.m@gmail.com>
  version_added: "0.1.0"
  short_description: 
  description:
    - This lookup returns the contents from a file on the Ansible controller's file system.
  notes:
    - if read in variable context, the file can be interpreted as YAML if the content is valid to the parser.
  options:
    _terms:
      required: True
      description: Folder ID
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
- ansible.builtin.set_fact:
    _yc_vpc_subnet_id: "{{ item.id }}"
  loop: "{{ lookup('ptsecurity.yandex_cloud.vpc_subnets', _yc_folder_id, iam_token=_yc_iam_token, wantlist=True) }}"
  when: "item.name == 'default'"
"""

RETURN = """
  _list:
    type: list
    elements: str
    description:
      - A list containing generated sequence of items
"""

import grpc
import yandexcloud

from datetime import datetime

from google.protobuf.json_format import MessageToDict

from yandex.cloud.vpc.v1.subnet_service_pb2_grpc import SubnetServiceStub
from yandex.cloud.vpc.v1.subnet_service_pb2 import ListSubnetsRequest

from ansible.errors import AnsibleError
from ansible.module_utils.common.text.converters import to_native
from ansible.plugins.lookup import LookupBase
from ansible.utils.display import Display

display = Display()


class LookupModule(LookupBase):
    def run(self, terms, variables=None, **kwargs):
        self.set_options(var_options=variables, direct=kwargs)

        results = []

        sdk = yandexcloud.SDK(
            interceptor=yandexcloud.RetryInterceptor(max_retry_count=3, retriable_codes=[grpc.StatusCode.UNAVAILABLE]),
            iam_token=self.get_option("iam_token"),
            token=self.get_option("token"),
            service_account_key=self.get_option("service_account_key")
        )
        service = sdk.client(SubnetServiceStub)

        for term in terms:
            if term == '':
                raise AnsibleError("Folder ID is required and can't be empty")

            display.vvvv("lookup subnet in folder id %r" % term)
            try:
                try:
                    service_return = service.List(ListSubnetsRequest(folder_id=term))
                except Exception as e:
                    raise AnsibleError(
                        "unknown error listing subnets in folder %r. Error was: %s" % (term, to_native(e))
                    )

                for subnet_dict in MessageToDict(service_return)["subnets"]:
                    subnet = {
                        "folder_id": subnet_dict["folderId"],
                        "id": subnet_dict["id"],
                        "name": subnet_dict["name"],
                        "description": subnet_dict["description"],
                        "network_id": subnet_dict["networkId"],
                        "route_table_id": subnet_dict["routeTableId"],
                        "zone_id": subnet_dict["zoneId"],
                        "created_at": int(
                            datetime.strptime(
                                subnet_dict["createdAt"] + "+0000", "%Y-%m-%dT%H:%M:%SZ%z"
                            ).timestamp()
                        ),
                        "v4_cidr_blocks": subnet_dict["v4CidrBlocks"],
                        "dhcp_options": {
                            "domain_name": subnet_dict["dhcpOptions"]["domainName"],
                            "domain_name_servers": subnet_dict["dhcpOptions"]["domainNameServers"],
                        }
                    }

                    results.append(subnet)
            except AnsibleError:
                raise
            except Exception as e:
                raise AnsibleError("unknown error formatting subnet dict: %s" % to_native(e))

        return results
