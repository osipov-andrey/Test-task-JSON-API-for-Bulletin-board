from rest_framework import viewsets, mixins

from .serializers import *


class BulletinsView(
    viewsets.GenericViewSet,
    mixins.ListModelMixin,
    mixins.CreateModelMixin,
    mixins.RetrieveModelMixin
):
    def list(self, request, *args, **kwargs):
        self.serializer_class = BulletinCreateSerializer
        return super().list(request, *args, **kwargs)

    def create(self, request, *args, **kwargs):
        self.serializer_class = BulletinCreateSerializer
        return super().create(request, *args, **kwargs)

    def retrieve(self, request, *args, **kwargs):
        params = self.request.query_params
        if 'fields' in params:
            self.serializer_class = BulletinFullDetailSerializer
            return super().retrieve(request, *args, **kwargs)
        self.serializer_class = BulletinDetailSerializer
        return super().retrieve(request, *args, **kwargs)

    def get_queryset(self):
        """ Sorting bulletins by URL-parameters """
        params = self.request.query_params
        if 'sort' in params:
            sorting_field = params['sort']
            if self.validate_sorting_field(sorting_field):
                if 'desc' in params:
                    sorting_field = '-' + sorting_field
                queryset = Bulletin.objects.all().order_by(sorting_field)
                return queryset
        queryset = Bulletin.objects.all()
        return queryset

    @staticmethod
    def validate_sorting_field(field_name: str):
        fields = [field.name for field in Bulletin._meta.fields]
        return field_name in fields
