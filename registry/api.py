import requests


class RegistryAPI(object):
    def __init__(self, host, insecure=False):
        self._registry = Registry(host, insecure)

    def is_registry_insecure(self):
        return self._registry.insecure

    def version_check(self):
        if self._registry.protocol == 'http':
            result = self._get_addressable_object(VersionCheck)
            if result:
                return result

        self._registry.protocol = 'https'
        return self._get_addressable_object(VersionCheck)

    def catalog(self, n=None, last=None):
        return self._get_addressable_object(Catalog(self._registry, n, last))

    def _get_addressable_object(self, objClass):
        url = "{}://{}{}".format(self._registry.protocol, self._registry.host, objClass.url)
        response = requests.get(url, verify=(not self._registry.insecure))
        return objClass.process_response(response)


class RegistryObject(object):
    pass


class AddressableRegistryObject(RegistryObject):
    version = "v2"

    @classmethod
    def process_response(cls, response):
        return response

class Registry(RegistryObject):
    def __init__(self, host, insecure):
        self.host = host
        self.insecure = insecure
        self.protocol = 'https'
        if self.insecure:
            self.protocol = 'http'

    def __repr__(self):
        return self.host

class Repository(RegistryObject):
    def __init__(self, registry, repository):
        self.registry = registry
        self.repository = repository

    def __repr__(self):
        return "{}/{}".format(self.registry, self.repository)


class Tag(RegistryObject):
    def __init__(self, repository, tag):
        self.repository = repository
        self.tag = tag

    def __repr__(self):
        return "{}:{}".format(self.repository, self.tag)


class VersionCheck(AddressableRegistryObject):
    url = '/{}/'.format(AddressableRegistryObject.version)

    @classmethod
    def process_response(cls, response):
        if response.status_code == 200:
            return True
        return False


class Catalog(AddressableRegistryObject):
    url = '/{}/_catalog'.format(AddressableRegistryObject.version)

    def __init__(self, registry):
        self.registry = registry

    def process_response(self, response):
        result = []
        for repo in response.json()['repositories']:
            result.append(Repository(self.registry, repo))
        return result


class Tags(AddressableRegistryObject):
    url = '/{}/{}/tags/list'.format(AddressableRegistryObject.version, "{}")

    def __init__(self, repository):
        self.repository = repository

    def process_response(self, response):
        result = []
        for tag in response.json()['tags']:
            result.append(Tag(self.repository, tag))
        return result
