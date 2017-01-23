## Python client library for Docker Registry v2

**Warning: This code is under development and will change in future version**

## Usage

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
