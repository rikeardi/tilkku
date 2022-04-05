from django.db import models
from django.utils.encoding import force_text
from django.core.serializers.json import DjangoJSONEncoder


class LazyEncoder(DjangoJSONEncoder):
    def default(self, obj):
#        if isinstance(obj, YourCustomType):
#            return force_text(obj)
        return super(LazyEncoder, self).default(obj)
