from django.db import models


# Create your models here.
@python_2_unicode_compatible
class Room(models.Model):
    title = models.CharField(max_length=255)

    def str(self):
        return self.title
