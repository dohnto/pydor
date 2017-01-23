import registry.api

import unittest
import requests_mock
import requests
import mock
import json
from os.path import expanduser


class TestApi(unittest.TestCase):
    def test_init(self):
        api = registry.api.API('localhost:5000')
        self.assertIsInstance(api, registry.api.API)

    @requests_mock.mock()
    def test_base(self, m):
        api = registry.api.API('localhost:5000', insecure=True)
        m.get('http://localhost:5000/v2/', text='{}')
        result = api.Base().get()
        self.assertEqual(result.status_code, requests.codes.ok)
        self.assertEqual(result.text, "{}")

    @requests_mock.mock()
    def test_catalog(self, m):
        api = registry.api.API('localhost:5000', insecure=True)
        m.get('http://localhost:5000/v2/_catalog', text='{"repositories":[]}')
        result = api.Catalog().get()
        self.assertEqual(result.status_code, requests.codes.ok)
        self.assertEqual(result.text, '{"repositories":[]}')

    @requests_mock.mock()
    def test_tags(self, m):
        api = registry.api.API('localhost:5000', insecure=True)
        m.get('http://localhost:5000/v2/a/tags/list', text='{"name":"a","tags":["latest"]}')
        result = api.Tags("a").get()
        self.assertEqual(result.status_code, requests.codes.ok)
        self.assertEqual(result.text, '{"name":"a","tags":["latest"]}')