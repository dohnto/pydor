import requests
import logging
import os.path
import json
import base64
import link_header
import collections

import registry

class API(object):
    def __init__(self, host, insecure=False, config_file="~/docker/config.json"):
        logging.debug("Creating new registry api: host=%s, insecure=%s, config_file=%s", host, insecure, config_file)
        self.registry = registry.Registry(host, insecure)

#         self.config_file = (config_file)
#         if self.config_file:
#             config_file_path = os.path.expanduser(config_file)
#             try:
#                 with open(config_file_path, 'r') as f:
#                     config_file = json.loads(f.read())
#                     try:
#                         auth = config_file["auths"][host]["auth"]
#                         self.user, self.password  = base64.b64decode(auth).split(":", 1)
#                     except KeyError:
#                         # something is missing, we ignore it
#                         pass
#             except IOError as e:
#                 logging.warn("Error while openning docker config file %s", e)
#
    def Base(self):
        return Base(self.registry)

    def Catalog(self):
        return Catalog(self.registry)

    def Tags(self, name):
        return Tags(self.registry, name)

    def Manifest(self, name, reference):
        return Manifest(self.registry, name, reference)

    def Blob(self, name, digest):
        return Blob(self.registry, name, digest)

    def InitiateBlobUpload(self, name):
        return InitiateBlobUpload(self.registry, name)

    def BlobUpload(self, name, uuid):
        return BlobUpload(self.registry, name, uuid)
#
class Entity(object):
    url = None

    def __init__(self, registry):
        self.registry = registry

    @property
    def url(self):
        return self.registry.url + self.relative_url

    @property
    def verify(self):
        return not self.registry.insecure

    def request(self, method, **kwargs):
        logging.debug("Calling %s: %s", method, self.url)
        return requests.request(method, self.url, verify=not self.registry.insecure, **kwargs)

    def get(self, *args, **kwargs):
        return self.request("GET", *args, **kwargs)

    def head(self, *args, **kwargs):
        return self.request("HEAD", *args, **kwargs)

    def post(self, *args, **kwargs):
        return self.request("POST", *args, **kwargs)

    def put(self, *args, **kwargs):
        return self.request("PUT", *args, **kwargs)

    def delete(self, *args, **kwargs):
        return self.request("DELETE", *args, **kwargs)


class Base(Entity):
    relative_url = "/v2/"

    def __init__(self, registry):
        Entity.__init__(self, registry)

class Catalog(Entity):
    relative_url = "/v2/_catalog"
    response_key = "repositories"

    def __init__(self, registry):
        Entity.__init__(self, registry)

    def __iter__(self):
        return EntityIterator(self.__class__, self.registry)

class EntityIterator(object):
    def __init__(self, cls, registry, *args, **kwargs):
        self.entity = cls(registry, *args, **kwargs)
        self.n = None
        self.next_is_stop = False
        self.cache = collections.deque()

    @property
    def params(self):
        params = {}
        if self.n is not None:
            params.update("n", self.n)
        return params

    def __next__(self):
        return self.next()

    def next(self):
        # if cache is empty, we grab more
        if len(self.cache) == 0:
            # in last iteration we found out that we reach the end
            if self.next_is_stop:
                raise StopIteration

            response = self.entity.get(params=self.params)
            self.cache = collections.deque(response.json()[self.entity.response_key])

            # if there is no more link, this is our last iteration
            # otherwise we parse the url for next iteration
            if "Link" not in response.headers:
                self.next_is_stop = True
            else:
                parsed_link = link_header.parse(response.headers["Link"]).links
                assert len(parsed_link) == 1
                self.entity.relative_url = parsed_link.pop().href

        return self.cache.popleft()


class Tags(Entity):
    relative_url = "/v2/{}/tags/list"
    response_key = "tags"

    def __init__(self, registry, name):
        Entity.__init__(self, registry)
        self.name = name
        self.relative_url = Tags.relative_url.format(self.name)

    def __iter__(self):
        return EntityIterator(self.__class__, self.registry, self.name)



class Manifest(Entity):
    relative_url = "/v2/{}/manifests/{}"

    def __init__(self, registry, name, reference):
        Entity.__init__(self, registry)
        self.name = name
        self.reference = reference
        self.relative_url = Manifest.relative_url.format(name, reference)


class Blob(Entity):
    relative_url = "/v2/{}/blobs/{}"

    def __init__(self, registry, name, digest):
        Entity.__init__(self, registry)
        self.name = name
        self.digest = digest
        self.relative_url = Manifest.relative_url.format(name, digest)


class InitiateBlobUpload(Entity):
    relative_url = "/v2/{}/blobs/uploads/"

    def __init__(self, registry, name):
        Entity.__init__(self, registry)
        self.name = name
        self.relative_url = Manifest.relative_url.format(name)


class BlobUpload(Entity):
    relative_url = "/v2/{}/blobs/{}"

    def __init__(self, registry, name, uuid):
        Entity.__init__(self, registry)
        self.name = name
        self.uuid = uuid
        self.relative_url = Manifest.relative_url.format(name, uuid)