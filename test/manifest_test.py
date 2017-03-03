import pydor.api
import pydor.manifest

import unittest
import requests_mock
import requests
import mock
import json
from os.path import expanduser


class TestManifest(unittest.TestCase):
    @requests_mock.mock()
    def test_quay_coreos_etcd_latest(self, m):
        api = pydor.api.API('quay.io')
        with open("test/mock/manifest/quay_io_v2_coreos_etcd_manifests_latest.json") as mock_response_file:
            mock_response = mock_response_file.read()
            m.get('https://quay.io/v2/coreos/etcd/manifests/latest', text=mock_response)
            manifest = pydor.Manifest(pydor.API("quay.io").Manifest("coreos/etcd", "latest").get())
            self.assertEqual([["/usr/local/bin/etcd"]], manifest.cmd.data)
            self.assertEqual([], manifest.entrypoint.data)
            self.assertEqual([], manifest.author.data)
            self.assertEqual([], manifest.labels.data)
