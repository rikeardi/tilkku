from django.db import models


# Create your models here.
class LayerType(models.TextChoices):
    AREA = 'AR', 'Alue'
    MARKER = 'MA', 'Merkintä'


class MapStyleManager(models.Manager):
    def get_by_natural_key(self, name):
        return self.get(name=name)


class MapStyle(models.Model):
    name = models.CharField(max_length=50)
    stroke = models.CharField(max_length=10)
    fill = models.CharField(max_length=10)
    opacity = models.FloatField()
    objects = MapStyleManager()

    def __str__(self):
        return f'{self.name}'


class Layer(models.Model):
    name = models.CharField(max_length=100)
    type = models.CharField(max_length=2, choices=LayerType.choices, default=LayerType.AREA)
    style = models.ForeignKey(MapStyle, on_delete=models.DO_NOTHING)
    objects = LayerManager()

    def __str__(self):
        return f'{self.name}'


class AreaManager(models.Manager):
    def get_by_natural_key(self, name):
        return self.get(name=name)


class Area(models.Model):
    name = models.CharField(max_length=200)
    layer = models.ForeignKey(Layer, related_name="areas", on_delete=models.DO_NOTHING)
    coordinates = models.TextField()
    objects = AreaManager()

    def __str__(self):
        return f'{self.name}'


class MarkerManager(models.Manager):
    def get_by_natural_key(self, name):
        return self.get(name=name)


class Marker(models.Model):
    name = models.CharField(max_length=200)
    layer = models.ForeignKey(Layer, related_name="markers", on_delete=models.DO_NOTHING)
    coordinates = models.TextField()
    objects = MarkerManager()

    def __str__(self):
        return f'{self.name}'


class MapServer(models.Model):
    name = models.CharField(max_length=100)
    url = models.CharField(max_length=500)
    attribution = models.CharField(max_length=300)

    def __str__(self):
        return f'{self.name}'

    def get_fields(self):
        return [(field.name, field.value_to_string(self)) for field in MapServer._meta.fields]
