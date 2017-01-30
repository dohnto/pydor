## Python client library for Docker Registry v2

**Warning: This code is under development and will change in future version**


## Docker image usage

```bash
$ docker run dohnto/pydor list --help
Usage: registryctl list [OPTIONS] REGISTRY

Options:
  --limit INTEGER                 number of namespaces to show
  --output [json|xls|yaml|csv|dbf|tsv|html|latex|xlsx|ods|txt]
                                  [default: txt]
  --insecure
  --help                          Show this message and exit.

$ docker run dohnto/pydor list quay.io
NAME
----------------------------
quay/elasticsearch
gilliam/base
gilliam/service-registry
modcloth/build-essential
...

$ docker run dohnto/pydor list --limit=1 quay.io
NAME
----------------------------
quay/elasticsearch

$ docker run dohnto/pydor list --output=json quay.io
[{"name": "quay/elasticsearch"}, {"name": "gilliam/base"}, ...]


$docker run dohnto/pydor tags quay.io/coreos/etcd
name
--------------
latest
test
v0.4.6
v0.4.8
v0.5.0_alpha.0
...

$ docker run dohnto/pydor inspect labels quay.io/dohnto/py-registry-client-demo:labels
name      |value
----------|-----
otherlabel|bar
mylabel   |foo

$ docker run dohnto/pydor inspect labels quay.io/dohnto/py-registry-client-demo@sha256:8f3a284c5761feb50a9b47939e492e261bde4eba1efe2e45a262d723f463a3bb
name      |value
----------|-----
otherlabel|bar
mylabel   |foo  
```


## registryctl usage

```bash
$ ./registryctl list --help
Usage: registryctl list [OPTIONS] REGISTRY

Options:
  --limit INTEGER                 number of namespaces to show
  --output [json|xls|yaml|csv|dbf|tsv|html|latex|xlsx|ods|txt]
                                  [default: txt]
  --insecure
  --help                          Show this message and exit.

$ ./registryctl list quay.io
NAME
----------------------------
quay/elasticsearch
gilliam/base
gilliam/service-registry
modcloth/build-essential
...

$ ./registryctl list --limit=1 quay.io
NAME
----------------------------
quay/elasticsearch

$ ./registryctl list --output=json quay.io
[{"name": "quay/elasticsearch"}, {"name": "gilliam/base"}, ...]


$ /registryctl tags quay.io/coreos/etcd
name
--------------
latest
test
v0.4.6
v0.4.8
v0.5.0_alpha.0
...

$ ./registryctl inspect labels quay.io/dohnto/py-registry-client-demo:labels
name      |value
----------|-----
otherlabel|bar
mylabel   |foo

$ ./registryctl inspect labels quay.io/dohnto/py-registry-client-demo@sha256:8f3a284c5761feb50a9b47939e492e261bde4eba1efe2e45a262d723f463a3bb
name      |value
----------|-----
otherlabel|bar
mylabel   |foo  
```

## library usage

Basic demo usage:

```python
#!/usr/bin/env python

import registry
registry_host = "localhost:5000"

api = registry.API(registry_host, insecure=True)
for repository in api.Catalog():
    for tag in api.Tags(repository):
        print("{}/{}:{}".format(registry_host, repository, tag))
```

Will produce
```
...
localhost:5000/a9:47
localhost:5000/a9:17
localhost:5000/a9:48
localhost:5000/a9:37
localhost:5000/a9:40
localhost:5000/a9:19
localhost:5000/a9:8
localhost:5000/a9:3
localhost:5000/a9:6
localhost:5000/a9:43
localhost:5000/a9:50
...
```
