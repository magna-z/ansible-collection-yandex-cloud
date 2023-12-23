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

from yandex.cloud.vpc.v1.subnet_service_pb2_grpc import SubnetServiceStub
from yandex.cloud.vpc.v1.subnet_service_pb2 import ListSubnetsRequest

from ansible.errors import AnsibleError
from ansible.module_utils.common.text.converters import to_native
from ansible.plugins.lookup import LookupBase
from ansible.utils.display import Display

from ..module_utils.common import message_to_dict
from ..module_utils.sdk import client

display = Display()


class LookupModule(LookupBase):
    def run(self, terms, variables=None, **kwargs):
        self.set_options(var_options=variables, direct=kwargs)

        results = list()

        service = client(
            SubnetServiceStub,
            iam_token=self.get_option('iam_token'),
            token=self.get_option('token'),
            service_account_key=self.get_option('service_account_key'),
        )

        for term in terms:
            if term == '':
                raise AnsibleError("Folder ID is required and can't be empty")

            display.vvvv("lookup subnet in folder id %r" % term)

            try:
                try:
                    response = service.List(ListSubnetsRequest(folder_id=term))
                except Exception as e:
                    raise AnsibleError(
                        "unknown error listing subnets in folder %r. Error was: %s" % (term, to_native(e))
                    )

                for subnet in message_to_dict(response)['subnets']:
                    results.append(subnet)

            except AnsibleError:
                raise
            except Exception as e:
                raise AnsibleError("unknown error formatting subnet dict: %s" % to_native(e))

        return results
