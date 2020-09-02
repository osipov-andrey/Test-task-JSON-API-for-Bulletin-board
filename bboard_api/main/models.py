from datetime import datetime

from django.core.exceptions import ValidationError
from django.db import models


class Bulletin(models.Model):
    name = models.CharField(max_length=200, verbose_name='Название объявления')
    price = models.IntegerField(verbose_name='Цена (в копейках)')
    main_photo = models.TextField(verbose_name='Ссылка на изображение')
    date = models.DateTimeField(
        auto_created=True, verbose_name='Дата создания', default=datetime.now()
    )

    description = models.TextField(max_length=1000, verbose_name='Описание объявления')

    def delete(self, *args, **kwargs):
        for ai in self.additionalimages.all():
            ai.delete()
        super().delete(*args, **kwargs)

    def additional_images(self):
        return self.additionalimages.all()

    class Meta:
        verbose_name = 'Объявление'
        verbose_name_plural = 'Объявления'


class AdditionalImage(models.Model):
    bulletin = models.ForeignKey(Bulletin, on_delete=models.CASCADE,
                                 verbose_name='Объявление', related_name='additionalimages')
    image = models.TextField(verbose_name='Ссылка на изображение')

    def clean(self):
        b = Bulletin.objects.get(pk=self.bulletin.pk)
        all_images = b.additionalimages.all()
        if len(all_images) >= 3:
            raise ValidationError('Too many images!')

    def save(self, *args, **kwargs):
        self.clean()
        super().save(*args, **kwargs)

    class Meta:
        verbose_name = 'Дополнительное изображение'
        verbose_name_plural = 'Дополнительные изображения'