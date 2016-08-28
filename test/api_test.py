import unittest
import registry.api
import requests_mock
import mock
import json
from os.path import expanduser

class TestApi(unittest.TestCase):
    def test_init(self):
        api = registry.api.RegistryAPI('localhost:5000')
        self.assertIsInstance(api, registry.RegistryAPI)
        self.assertFalse(api.is_registry_insecure())

    def test_init_insecure(self):
        api = registry.api.RegistryAPI('localhost:5000', insecure=True)
        self.assertIsInstance(api, registry.RegistryAPI)
        self.assertTrue(api.is_registry_insecure())


class TestVersionCheck(unittest.TestCase):
    @requests_mock.Mocker()
    def test_version_check_200(self, m):
        m.get('https://localhost:5000/v2/', text='{}', status_code=200)
        api = registry.api.RegistryAPI('localhost:5000')
        self.assertTrue(api.version_check())

    @requests_mock.Mocker()
    def test_version_check_404(self, m):
        m.get('https://localhost:5000/v2/', text='{}', status_code=404)
        api = registry.api.RegistryAPI('localhost:5000')
        self.assertFalse(api.version_check())

    @requests_mock.Mocker()
    def test_version_check_insecure_404(self, m):
        m.get('http://localhost:5000/v2/', text='{}', status_code=404)
        m.get('https://localhost:5000/v2/', text='{}', status_code=404)
        api = registry.api.RegistryAPI('localhost:5000', insecure=True)
        self.assertFalse(api.version_check())

    @requests_mock.Mocker()
    def test_version_check_insecure_200(self, m):
        m.get('http://localhost:5000/v2/', text='{}', status_code=200)
        api = registry.api.RegistryAPI('localhost:5000', insecure=True)
        self.assertTrue(api.version_check())

    @requests_mock.Mocker()
    def test_version_check_insecure_200_https(self, m):
        m.get('http://localhost:5000/v2/', text='{}', status_code=404)
        m.get('https://localhost:5000/v2/', text='{}', status_code=200)
        api = registry.api.RegistryAPI('localhost:5000', insecure=True)
        self.assertTrue(api.version_check())


class Catalog(object):
    def __init__(self):
        self.repos = ["quay/elasticsearch", "gilliam/base", "gilliam/service-registry", "modcloth/build-essential", "modcloth/nodejs-dev", "modcloth/hubot", "modcloth/ruby-dev", "modcloth/ruby2-dev", "darron/docker-nginx-php5", "darron/docker-chef-omnibus", "darron/cedarish", "darron/docker-redis", "noteed/ubuntu", "modcloth/postgresql-pgdg", "modcloth/postgresql-93", "modcloth/docker-build-worker", "modcloth/ohhai", "dhrp/znc", "modcloth/percona-apt-repo", "scottbessler/oracle-java6", "ZlotaLza/Translate-Discourse", "kencochrane/test", "kencochrane/test-repo", "octohost/nodejs", "yawnt/derpo", "docplanner/php", "fermayo/test", "conradev/squid", "fermayo/ubuntu", "jdmo/testme", "niallo/stridercd", "modcloth/percona-56", "signalfuse/kafka", "signalfuse/zookeeper", "rfjimen/testing", "datacratic/datacratic-ubuntu", "nils/barkeep", "cardmagic/foobar", "emilebosch/rails-base", "abierbaum/ping", "namin/livecode", "ihtsdo/snomed-solr", "emilebosch/polybox-rails", "abierbaum/tag_test", "abierbaum/test_area", "michiels/intercity", "jarosser06/magic", "blindly/hhvm", "blindly/lamp", "mindmorass/0002demo"]

    def response_all(self):
        return self.dump(self.repos)

    def dump(self, repos):
        return json.dumps({"repositories": repos})

    def response(self, n, last):
        repos = []
        found = False
        for i in self.repos:
            if i == last:
                found = True
            if found:
                repos.append(i)
            if len(repos) == n:
                break
        return self.dump(repos)


class TestCatalog(unittest.TestCase):
    @requests_mock.Mocker()
    def test_catalog_5(self, m):
        c = Catalog()
        m.get('https://quay.io/v2/_catalog', text=c.response_all(), status_code=200)
        api = registry.api.RegistryAPI('quay.io')
        n = 5
        catalog = api.catalog(n)
        self.assertEqual(len(catalog), len(c.repos))
        
if __name__ == '__main__':
    unittest.main()
