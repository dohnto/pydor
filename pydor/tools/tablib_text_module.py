title = 'txt'
extensions = ('txt',)

DEFAULT_DELIMITER = '\n'


def export_set(dataset, **kwargs):
    return dataset


def import_set(dset, in_stream, headers=True, **kwargs):
    raise NotImplemented()


def detect(stream, delimiter=DEFAULT_DELIMITER):
    raise NotImplemented()
