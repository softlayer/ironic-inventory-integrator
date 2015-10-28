from wsme import types as wtypes
from wsmeext import pecan as wsme_pecan

__author__ = 'chaustin'


class ApiBase(wtypes.Base):
    """A Base Object for handling serialization of objects from request
    """

    def as_dict(self):
        return {field: getattr(self, field) for field in self.fields}


def wsme_expose(*args, **kwargs):
    """Coerce the content type to json"""

    if 'rest_content_types' not in kwargs:
        kwargs['rest_content_types'] = ('json', )
    return wsme_pecan.wsexpose(*args, **kwargs)