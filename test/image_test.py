import pydor.image

import unittest


class TestImagePositive(unittest.TestCase):
    def test_parsing_basic(self):
        image = pydor.image.Image.from_image("registry.dev/aaa:bbb")
        self.assertEqual(image.registry, "registry.dev")
        self.assertEqual(image.repository, "aaa")
        self.assertEqual(image.tag, "bbb")
        self.assertEqual(image.digest, None)

    def test_parsing_no_tag_latest(self):
        image = pydor.image.Image.from_image("registry.dev/aaa")
        self.assertEqual(image.registry, "registry.dev")
        self.assertEqual(image.repository, "aaa")
        self.assertEqual(image.tag, "latest")
        self.assertEqual(image.digest, None)

    def test_parsing_no_tag(self):
        image = pydor.image.Image.from_image("registry.dev/aaa", None)
        self.assertEqual(image.registry, "registry.dev")
        self.assertEqual(image.repository, "aaa")
        self.assertEqual(image.tag, None)
        self.assertEqual(image.digest, None)

    def test_parsing_nested_namespace(self):
        image = pydor.image.Image.from_image("registry.dev/aaa/bbb/ccc:123")
        self.assertEqual(image.registry, "registry.dev")
        self.assertEqual(image.repository, "aaa/bbb/ccc")
        self.assertEqual(image.tag, "123")
        self.assertEqual(image.digest, None)

    def test_parsing_registry_with_port(self):
        image = pydor.image.Image.from_image("registry.dev:3000/aaa/bbb/ccc:123")
        self.assertEqual(image.registry, "registry.dev:3000")
        self.assertEqual(image.repository, "aaa/bbb/ccc")
        self.assertEqual(image.tag, "123")
        self.assertEqual(image.digest, None)

    def test_parsing_localhost_with_port(self):
        image = pydor.image.Image.from_image("localhost:3000/aaa/bbb/ccc:123")
        self.assertEqual(image.registry, "localhost:3000")
        self.assertEqual(image.repository, "aaa/bbb/ccc")
        self.assertEqual(image.tag, "123")
        self.assertEqual(image.digest, None)

    def test_parsing_localhost2_with_port(self):
        image = pydor.image.Image.from_image("127.0.0.1:3000/aaa/bbb/ccc:123")
        self.assertEqual(image.registry, "127.0.0.1:3000")
        self.assertEqual(image.repository, "aaa/bbb/ccc")
        self.assertEqual(image.tag, "123")
        self.assertEqual(image.digest, None)

    def test_parsing_localhost_without_port(self):
        image = pydor.image.Image.from_image("localhost/aaa/bbb/ccc:123")
        self.assertEqual(image.registry, "localhost")
        self.assertEqual(image.repository, "aaa/bbb/ccc")
        self.assertEqual(image.tag, "123")
        self.assertEqual(image.digest, None)

    def test_parsing_docker_hub_image(self):
        image = pydor.image.Image.from_image("aaa/bbb:ccc")
        self.assertEqual(image.registry, None)
        self.assertEqual(image.repository, "aaa/bbb")
        self.assertEqual(image.tag, "ccc")
        self.assertEqual(image.digest, None)

    def test_parsing_docker_hub_image_without_tag(self):
        image = pydor.image.Image.from_image("aaa/bbb")
        self.assertEqual(image.registry, None)
        self.assertEqual(image.repository, "aaa/bbb")
        self.assertEqual(image.tag, "latest")
        self.assertEqual(image.digest, None)

    def test_parsing_docker_hub_image_without_namespace(self):
        image = pydor.image.Image.from_image("debian")
        self.assertEqual(image.registry, None)
        self.assertEqual(image.repository, "debian")
        self.assertEqual(image.tag, "latest")
        self.assertEqual(image.digest, None)

    def test_parsing_docker_hub_image_without_namespace_with_tag(self):
        image = pydor.image.Image.from_image("debian:wheezy")
        self.assertEqual(image.registry, None)
        self.assertEqual(image.repository, "debian")
        self.assertEqual(image.tag, "wheezy")
        self.assertEqual(image.digest, None)

    def test_parsing_docker_hub_image_without_namespace_with_zero_tag(self):
        image = pydor.image.Image.from_image("debian:0")
        self.assertEqual(image.registry, None)
        self.assertEqual(image.repository, "debian")
        self.assertEqual(image.tag, "0")
        self.assertEqual(image.digest, None)

    def test_parsing_digest_basic(self):
        image = pydor.image.Image.from_image("abc.test/xyz@sha256:123")
        self.assertEqual(image.registry, "abc.test")
        self.assertEqual(image.repository, "xyz")
        self.assertEqual(image.tag, None)
        self.assertEqual(image.digest, "sha256:123")

    def test_parsing_registry(self):
        image = pydor.image.Image.from_image("localhost:5000")
        self.assertEqual(image.registry, "localhost:5000")
        self.assertEqual(image.repository, None)
        self.assertEqual(image.tag, None)
        self.assertEqual(image.digest, None)

    def test_parsing_registry2(self):
        image = pydor.image.Image.from_image("localhost:5000/a", latest_tag_if_empty=None)
        self.assertEqual(image.registry, "localhost:5000")
        self.assertEqual(image.repository, "a")
        self.assertEqual(image.tag, None)
        self.assertEqual(image.digest, None)

class TestImageNegative(unittest.TestCase):
    def test_parsing_basic(self):
        with self.assertRaises(AttributeError):
            pydor.image.Image.from_image("registry.dev/aa|a:bbb")