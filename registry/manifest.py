import json
import logging

MANIFEST_PROPERTIES = ["labels", "author", "entrypoint", "cmd"]

class ManifestItem(object):
    def __init__(self, headers, data=None):
        self.headers = headers
        self._data = data

    @property
    def data(self):
        return filter(lambda row: row[0] is not None, self._data)


class Labels(ManifestItem):
    def __init__(self, data):
        super(Labels, self).__init__(["name", "value"], data)

class Author(ManifestItem):
    def __init__(self, data):
        super(Author, self).__init__(["author"], [[data]])

class Entrypoint(ManifestItem):
    def __init__(self, data):
        super(Entrypoint, self).__init__(["entrypoint"], map(lambda i: [i], data))

class Cmd(ManifestItem):
    def __init__(self, data):
        super(Cmd, self).__init__(["cmd"], map(lambda i: [i], data))

class Manifest(object):
    def __init__(self, obj):
        self.obj = obj
        self._labels = None
        self._author = None
        self._entrypoint = None
        self._cmd = None
        self._json = None
        self._history_latest_layer = None

    @property
    def json(self):
        if self._json is None:
            self._json = self.obj.json()
        return self._json

    @property
    def history_latest_layer(self):
        if self._history_latest_layer is None:
            self._history_latest_layer = json.loads(self.json["history"][0]['v1Compatibility'])
        return self._history_latest_layer

    @property
    def labels(self):
        if self._labels is None:
            self._labels = self.history_latest_layer['config']['Labels']
        return Labels(map(lambda k: [k, self._labels[k]], self._labels))

    @property
    def author(self):
        if self._author is None:
            try:
                self._author = self.history_latest_layer['author']
            except KeyError as e:
                self._author = None
        return Author(self._author)

    @property
    def entrypoint(self):
        if self._entrypoint is None:
            try:
                self._entrypoint = self.history_latest_layer['config']['Entrypoint']
            except KeyError as e:
                self._entrypoint = None
        print(self._entrypoint)
        return Entrypoint(self._entrypoint)

    @property
    def cmd(self):
        if self._cmd is None:
            try:
                self._cmd = self.history_latest_layer['config']['Cmd']
            except KeyError as e:
                self._cmd = None
        return Cmd(self._cmd)