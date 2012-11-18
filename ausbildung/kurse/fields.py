
from django.db.models import CharField

class RequiredCharField(CharField):
    def __init__(self, *args, **kwargs):
            kwargs['max_length'] = kwargs.get('max_length', 100)
            CharField.__init__(self, *args, **kwargs)

class OptionalCharField(CharField):
    def __init__(self, *args, **kwargs):
            kwargs['max_length'] = kwargs.get('max_length', 100)
            kwargs['blank'] = kwargs.get('blank', True)
            kwargs['null'] = kwargs.get('null', True)
            CharField.__init__(self, *args, **kwargs)
