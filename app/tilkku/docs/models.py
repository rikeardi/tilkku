from django.db import models


# Create your models here.
class DocsHeader(models.Model):
    title = models.CharField(max_length=100)
    order = models.IntegerField(default=0)

    class Meta:
        ordering = ['order']

    def __str__(self):
        return f'{self.title}'


class DocsPage(models.Model):
    header = models.ForeignKey(DocsHeader, on_delete=models.CASCADE)
    title = models.CharField(max_length=100)

    class Meta:
        ordering = ['title']

    def __str__(self):
        return f'{self.title}'


class DocsChapter(models.Model):
    page = models.ForeignKey(DocsPage, on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    order = models.IntegerField(default=0)

    class Meta:
        ordering = ['order']

    def __str__(self):
        return f'{self.title}'


class DocsSection(models.Model):
    chapter = models.ForeignKey(DocsChapter, on_delete=models.CASCADE)
    order = models.IntegerField(default=0)
    text = models.TextField(blank=True, default='')
    image = models.TextField(blank=True, default='')
    image_type = models.CharField(max_length=20, blank=True, default='')
    image_name = models.CharField(max_length=250, blank=True, default='')

    class Meta:
        ordering = ['order']

    def __str__(self):
        if self.text:
            if len(self.text) > 100:
                text = self.text[:100] + '...'
            else:
                text = self.text
            return f'{text}'
        elif self.image:
            return f'{self.chapter.title} - image {self.order}'
