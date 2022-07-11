from django.db import models


# Create your models here.
class LayerType(models.TextChoices):
    AREA = 'AR', 'Alue'
    MARKER = 'MA', 'Merkintä'


class TopicStatus(models.TextChoices):
    OPEN = 'OP', 'Avoin'
    CLOSED = 'CL', 'Suljettu'


class MapStyle(models.Model):
    name = models.CharField(max_length=50)
    stroke = models.CharField(max_length=10)
    fill = models.CharField(max_length=10)
    opacity = models.FloatField()
    min_zoom = models.IntegerField(default=5)
    max_zoom = models.IntegerField(default=16)
    font_size = models.IntegerField(default=18)
    stroke_width = models.FloatField(default=2)

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
    coordinates = models.JSONField()

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


class Note(models.Model):
    header = models.CharField(max_length=200)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey('auth.User', on_delete=models.CASCADE)
    site = models.ForeignKey(Site, on_delete=models.DO_NOTHING, blank=True, null=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f'{self.topic}'


class Topic(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True, default='')
    status = models.CharField(max_length=100, choices=TopicStatus.choices, default=TopicStatus.OPEN)
    notes = models.ManyToManyField(Note, blank=True)

    class Meta:
        ordering = ['name']

    def __str__(self):
        return f'{self.name}'
