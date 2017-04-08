class EntityNotFound(ValueError): pass
class TagNotFound(EntityNotFound): pass
class RepoNotFound(EntityNotFound): pass

SSL_ERROR_CODE = 1
ENTITY_NOT_FOUND = 2
NOT_V2_REGISTRY = 3
IMAGE_NOT_FOUND = 4
NOT_IMPLEMENTED = 255