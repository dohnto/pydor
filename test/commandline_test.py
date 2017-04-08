import pydor.commandline
import pydor.errors

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

    @requests_mock.mock()
    def test_tags_empty(self, m):
        api = pydor.api.API('registry.test')
        with open("test/mock/manifest/list_tags_empty.json") as mock_response_file:
            mock_response = mock_response_file.read()
            m.get('https://registry.test/v2/generic/foo/tags/list', text=mock_response)

            runner = click.testing.CliRunner()
            result = runner.invoke(pydor.commandline.tags, ["--output", "json", "registry.test/generic/foo"])
            self.assertEqual(result.exit_code, 0)
            self.assertEqual(result.output, "[]\n")

    @requests_mock.mock()
    def test_inspect_exists(self, m):
        runner = click.testing.CliRunner()

        with open("test/mock/manifest/existing_image.json") as mock_response_file:
            mock_response = mock_response_file.read()
            m.get('https://registry.test/v2/generic/foo/manifests/x', text=mock_response)
            result_existing = runner.invoke(pydor.commandline.exists, ["registry.test/generic/foo:x"])
            self.assertEqual(result_existing.exit_code, 0)

        with open("test/mock/manifest/non_existing_image.json") as mock_response_file:
            mock_response = mock_response_file.read()
            m.get('https://registry.test/v2/generic/foo/manifests/y', text=mock_response, status_code=404)
            result_existing = runner.invoke(pydor.commandline.exists, ["registry.test/generic/foo:y"])
            self.assertEqual(result_existing.exit_code, pydor.errors.IMAGE_NOT_FOUND)