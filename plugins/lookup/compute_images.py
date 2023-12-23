from __future__ import (absolute_import, division, print_function)
__metaclass__ = type

DOCUMENTATION = """
  name: compute_images
  author: Maxim Zalysin <zalysin.m@gmail.com>
  version_added: "0.1.0"
  short_description: 
  description:
    - 
  notes:
    - 
  options:
    _terms:
      required: True
      description: Image family
    folder_id:
      type: string
      default: standard-images
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
- ansible.builtin.set_fact:
    _yc_compute_image: "{{ lookup('yandex.cloud.compute_images', 'debian-11', iam_token=_yc_iam_token) }}"
"""

RETURN = """
  _list:
    type: list
    elements: str
    description:
      - A list containing generated sequence of items
"""

from yandex.cloud.compute.v1.image_service_pb2_grpc import ImageServiceStub
from yandex.cloud.compute.v1.image_service_pb2 import GetImageLatestByFamilyRequest

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
            ImageServiceStub,
            iam_token=self.get_option('iam_token'),
            token=self.get_option('token'),
            service_account_key=self.get_option('service_account_key'),
        )

        folder_id = self.get_option('folder_id')

        for term in terms:
            if len(term.strip()) == 0:
                raise AnsibleError("Image family is required and can't be empty")

            display.vvvv("lookup latest image by family %r" % term)

            try:
                try:
                    image = service.GetLatestByFamily(
                        GetImageLatestByFamilyRequest(folder_id=folder_id, family=term)
                    )
                except Exception as e:
                    raise AnsibleError(
                        "unknown error getting image latest by family %r in folder %r. Error was: %s"
                        % (term, folder_id, to_native(e))
                    )

                results.append(message_to_dict(image))

            except AnsibleError:
                raise
            except Exception as e:
                raise AnsibleError("unknown error formatting image dict: %s" % to_native(e))

        return results
