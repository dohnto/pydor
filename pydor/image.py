import logging

LATEST_TAG="latest"

class Image(object):
    def __init__(self, registry, repository, tag=None, digest=None):
        self.registry = registry
        self.repository = repository
        self.tag = tag
        self.digest = digest
        assert self.digest is None or self.tag is None

    @property
    def reference(self):
        return self.digest or self.tag

    def __repr__(self):
        result = ""
        if self.registry:
            result += self.registry + "/"
        if self.repository:
            result += self.repository
        if self.tag:
            result += ":" + self.tag
        if self.digest:
            result+= "@" + self.digest
        return result

    @staticmethod
    def from_image(image, latest_tag_if_empty=LATEST_TAG):
        registry, repository, tag, digest = None, None, None, None

        domain_split_point = image.find('.')
        host_split_point = image.find('/')

        # we have found a dot and it is before slash => slash deliminates registry
        if domain_split_point != -1 and domain_split_point < host_split_point:
            registry = image[:host_split_point]
            rest = image[host_split_point+1:]
        elif image.startswith("localhost:") or image.startswith("localhost/"):
            registry = image[:host_split_point]
            rest = image[host_split_point+1:]
        else:
            rest = image

        # we must test digest occurence before tag
        digest_split_point = rest.find('@')
        if digest_split_point == -1:
            # there is no digest so there might be a tag
            tag_split_point = rest.find(':')
            if tag_split_point == -1:
                repository = rest
                if latest_tag_if_empty:
                    tag = latest_tag_if_empty
            else:
                repository = rest[:tag_split_point]
                tag = rest[tag_split_point+1:]
        else:
            repository = rest[:digest_split_point]
            digest = rest[digest_split_point+1:]

        assert repository != ''

        return Image(registry, repository, tag, digest)