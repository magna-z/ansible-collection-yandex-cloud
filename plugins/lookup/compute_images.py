from __future__ import (absolute_import, division, print_function)
__metaclass__ = type

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

from yandex.cloud.compute.v1.image_service_pb2_grpc import ImageServiceStub
from yandex.cloud.compute.v1.image_service_pb2 import GetImageLatestByFamilyRequest

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
        service = sdk.client(ImageServiceStub)
        folder_id = self.get_option("folder_id")

        for term in terms:
            if len(term.strip()) == 0:
                raise AnsibleError("Image family is required and can't be empty")

            display.vvvv("lookup latest image by family %r" % term)

            try:
                try:
                    service_return = service.GetLatestByFamily(
                        GetImageLatestByFamilyRequest(folder_id=folder_id, family=term)
                    )
                except Exception as e:
                    raise AnsibleError(
                        "unknown error getting image latest by family %r in folder %r. Error was: %s"
                        % (term, folder_id, to_native(e))
                    )

                image_dict = MessageToDict(service_return)
                image = {
                    "folder_id": image_dict["folderId"],
                    "family": image_dict["family"],
                    "id": image_dict["id"],
                    "name": image_dict["name"],
                    "description": image_dict["description"],
                    "size": int(image_dict["storageSize"]),
                    "min_disk_size": int(image_dict["minDiskSize"]),
                    "created_at": int(
                        datetime.strptime(
                            image_dict["createdAt"] + "+0000", "%Y-%m-%dT%H:%M:%SZ%z"
                        ).timestamp()
                    ),
                    "os_type": image_dict["os"]["type"],
                    "product_ids": image_dict["productIds"],
                    "status": image_dict["status"],
                    "pooled": bool(image_dict["pooled"]),
                }

                results.append(image)

            except AnsibleError:
                raise
            except Exception as e:
                raise AnsibleError("unknown error formatting image dict: %s" % to_native(e))

        return results
