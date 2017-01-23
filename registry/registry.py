class Registry(object):
    def __init__(self, host, insecure):
        self.host = host
        self.protocol = 'http' if insecure else 'https'
        self.insecure = insecure

    @property
    def url(self):
        return "{}://{}".format(self.protocol, self.host)
