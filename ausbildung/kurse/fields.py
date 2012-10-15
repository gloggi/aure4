
from django.db.models import CharField

class Required(CharField):
    def __init__(self, *args, **kwargs):
            kwargs['max_length'] = kwargs.get('max_length', 100)
            CharField.__init__(self, *args, **kwargs)

class Optional(CharField):
    def __init__(self, *args, **kwargs):
            kwargs['max_length'] = kwargs.get('max_length', 100)
            kwargs['blank'] = kwargs.get('blank', True)
            kwargs['null'] = kwargs.get('null', True)
            CharField.__init__(self, *args, **kwargs)
