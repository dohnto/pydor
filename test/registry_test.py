import pydor.registry

import unittest
import requests_mock
import mock
import json
from os.path import expanduser


class TestRegistry(unittest.TestCase):
    def test_registry_insecure(self):
        r = pydor.registry.Registry('localhost:5000', True)
        self.assertIsInstance(r, pydor.registry.Registry)
        self.assertEqual(r.host, 'localhost:5000')
        self.assertTrue(r.insecure)
        self.assertEqual(r.protocol, "http")
        self.assertEqual(r.url, "http://localhost:5000")

    def test_registry_secure(self):
        r = pydor.registry.Registry('localhost:5000', False)
        self.assertIsInstance(r, pydor.registry.Registry)
        self.assertEqual(r.host, 'localhost:5000')
        self.assertFalse(r.insecure)
        self.assertEqual(r.protocol, "https")
        self.assertEqual(r.url, "https://localhost:5000")
