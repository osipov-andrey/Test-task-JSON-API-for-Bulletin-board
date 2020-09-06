from datetime import datetime

from .models import Bulletin, AdditionalImage
from rest_framework import serializers
from drf_writable_nested.serializers import WritableNestedModelSerializer


class AdditionalImageSerializer(serializers.HyperlinkedModelSerializer):
    """ Сериалайзер доп.изображения для объявления """
    class Meta:
        model = AdditionalImage
        fields = ('image', )


class BulletinCreateSerializer(WritableNestedModelSerializer):
    date = serializers.HiddenField(default=datetime.now())
    additionalimages = AdditionalImageSerializer(many=True, allow_null=True, required=False)

    def validate_additionalimages(self, data):
        """ Нельзя добавлять более 3 доп.изображений """
        if len(data) > 3:
            raise serializers.ValidationError('Too many images! Max: 3')

    def validate_name(self, data):
        if len(data) > 200:
            raise serializers.ValidationError('Too long Name!')
        else:
            return data

    class Meta:
        model = Bulletin
        fields = '__all__'


class BulletinDetailSerializer(serializers.ModelSerializer):
    """ Shortcut serializer for viewing bulletin """
    class Meta:
        model = Bulletin
        fields = ('name', 'price', 'main_photo')


class BulletinFullDetailSerializer(BulletinDetailSerializer):
    """ Serializer for viewing bulletin with all fields """
    additionalimages = AdditionalImageSerializer(many=True, allow_null=True, required=False)

    class Meta:
        model = Bulletin
        fields = '__all__'


class BulletinListSerializer(serializers.ModelSerializer):
    """ Bulletins list serializer. Pagination enabled (in settings.py) """
    class Meta:
        model = Bulletin
        fields = ('name', 'main_photo', 'price')



