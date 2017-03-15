import pydor.commandline

import unittest
import click.testing
import requests_mock


class TestCommandline(unittest.TestCase):
    @requests_mock.mock()
    def test_tags_non_existing(self, m):
        api = pydor.api.API('registry.test')
        with open("test/mock/manifest/list_tags_name_unknown.json") as mock_response_file:
            mock_response = mock_response_file.read()
            m.get('https://registry.test/v2/devops/fluentd/tags/list', text=mock_response)

            runner = click.testing.CliRunner()
            result = runner.invoke(pydor.commandline.tags, ["--output", "json", "registry.test/devops/fluentd"])
            self.assertEqual(result.exit_code, 2)
            self.assertEqual(result.output, "NAME_UNKNOWN: repository name not known to registry (devops/fluentd)\n")