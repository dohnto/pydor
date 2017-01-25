## Python client library for Docker Registry v2

**Warning: This code is under development and will change in future version**

## registryctl usage

```bash
$ ./registryctl list localhost:5000
Usage: registryctl list [OPTIONS] REGISTRY

Options:
  --limit INTEGER                 number of greetings
  --output [text|json|yaml|html|csv]
  --insecure
  --help                          Show this message
                                  and exit.

$ ./registryctl list localhost:5000
- name/space1
- name/space2
...

$ ./registryctl list --limit=1 localhost:5000
- name/space1

$ ./registryctl list --output=json localhost:5000
[{"name": "name/space1"}, {"name": "name/space2"} ... ]

$ ./registryctl tags localhost:5000 name/space1
- latest
- v1
- v2
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
