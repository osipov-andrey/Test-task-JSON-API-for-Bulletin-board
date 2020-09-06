from datetime import datetime

from django.db import models


class Bulletin(models.Model):
    name = models.CharField(max_length=200, verbose_name='Bulletin name')
    price = models.PositiveIntegerField(verbose_name='Price (cents)')
    main_photo = models.URLField(verbose_name='Hyperlink to image')
    date = models.DateTimeField(
        auto_created=True, verbose_name='Date of creation', default=datetime.now()
    )
    description = models.TextField(max_length=1000, verbose_name='Bulletin description')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Bulletin'
        verbose_name_plural = 'Bulletins'


class AdditionalImage(models.Model):
    bulletin = models.ForeignKey(Bulletin, on_delete=models.CASCADE,
                                 verbose_name='Bulletin', related_name='additionalimages')
    image = models.URLField(verbose_name='Hyperlink to main image')

    class Meta:
        verbose_name = 'Additional image'
        verbose_name_plural = 'Additional images'
