from datetime import datetime

from .models import Bulletin, AdditionalImage
from rest_framework import serializers
from drf_writable_nested.serializers import WritableNestedModelSerializer


class AdditionalImageSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = AdditionalImage
        fields = ('image', )

    # def validate(self, data):
    #     print(data)
    #     pk = data['pk']
    #     b = Bulletin.objects.get(pk=pk)
    #     all_images = b.additionalimages.all()
    #     if len(all_images) >= 3:
    #         raise serializers.ValidationError('Too many images!')


class BulletinDetailSerializer(WritableNestedModelSerializer):
    date = serializers.HiddenField(default=datetime.now())
    additionalimages = AdditionalImageSerializer(many=True, allow_null=True, required=False)

    class Meta:
        model = Bulletin
        fields = ('name', 'main_photo', 'price', 'additionalimages', 'date')


class BulletinListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Bulletin
        fields = ('name', 'main_photo', 'price')



