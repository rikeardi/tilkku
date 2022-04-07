from django.db import models


# Create your models here.
class LayerType(models.TextChoices):
    AREA = 'AR', 'Alue'
    MARKER = 'MA', 'Merkintä'


class MapStyle(models.Model):
    name = models.CharField(max_length=50)
    stroke = models.CharField(max_length=10)
    fill = models.CharField(max_length=10)
    opacity = models.FloatField()

    def __str__(self):
        return f'{self.name}'


class Layer(models.Model):
    name = models.CharField(max_length=100)
    type = models.CharField(max_length=2, choices=LayerType.choices, default=LayerType.AREA)
    style = models.ForeignKey(MapStyle, on_delete=models.DO_NOTHING)

    def __str__(self):
        return f'{self.name}'


class Area(models.Model):
    name = models.CharField(max_length=200)
    layer = models.ForeignKey(Layer, to_field="areas", on_delete=models.DO_NOTHING)
    coordinates = models.TextField()

    def __str__(self):
        return f'{self.name}'


class Marker(models.Model):
    name = models.CharField(max_length=200)
    layer = models.ForeignKey(Layer, to_field="markers", on_delete=models.DO_NOTHING)
    coordinates = models.TextField()

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
