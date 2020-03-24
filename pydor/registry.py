class Registry(object):
    def __init__(self, host, insecure, verify_tls=None):
        self.host = host
        self.protocol = 'http' if insecure else 'https'
        self.insecure = insecure
        self.verify_tls = verify_tls if verify_tls is not None else not insecure

    @property
    def url(self):
        return "{}://{}".format(self.protocol, self.host)
