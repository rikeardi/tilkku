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
    min_zoom = models.IntegerField(default=5)
    max_zoom = models.IntegerField(default=16)
    font_size = models.IntegerField(default=18)
    stroke_width = models.FloatField()

    class Meta:
        ordering = ['name']

    def __str__(self):
        return f'{self.name}'


class Layer(models.Model):
    name = models.CharField(max_length=100)
    type = models.CharField(max_length=2, choices=LayerType.choices, default=LayerType.AREA)
    style = models.ForeignKey(MapStyle, on_delete=models.DO_NOTHING)

    class Meta:
        ordering = ['name']

    def __str__(self):
        return f'{self.name}'


class Area(models.Model):
    name = models.CharField(max_length=200)
    subtitle = models.CharField(max_length=300, blank=True, default='')
    layer = models.ForeignKey(Layer, related_name="areas", on_delete=models.DO_NOTHING)
    coordinates = models.JSONField()

    class Meta:
        ordering = ['name']

    def __str__(self):
        return f'{self.name}'


class Marker(models.Model):
    name = models.CharField(max_length=200)
    layer = models.ForeignKey(Layer, related_name="markers", on_delete=models.DO_NOTHING)
    coordinates = models.TextField()

    class Meta:
        ordering = ['name']

    def __str__(self):
        return f'{self.name}'


class MapServer(models.Model):
    name = models.CharField(max_length=100)
    url = models.CharField(max_length=500)
    attribution = models.CharField(max_length=300)

    def __str__(self):
        return f'{self.name}'


class SiteCategory(models.Model):
    name = models.CharField(max_length=100)

    class Meta:
        ordering = ['name']

    def __str__(self):
        return f'{self.name}'


class Site(models.Model):
    name = models.CharField(max_length=100)
    area = models.ForeignKey(Area, on_delete=models.DO_NOTHING, blank=True, null=True)
    marker = models.ForeignKey(Marker, on_delete=models.DO_NOTHING, blank=True, null=True)
    category = models.ForeignKey(SiteCategory, on_delete=models.DO_NOTHING)
    description = models.TextField(blank=True, default='')

    class Meta:
        ordering = ['name']

    def __str__(self):
        return f'{self.name}'
