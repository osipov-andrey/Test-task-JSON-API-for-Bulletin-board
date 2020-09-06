from rest_framework import viewsets, mixins

from .serializers import *


class BulletinCreateView(viewsets.GenericViewSet, mixins.ListModelMixin, mixins.CreateModelMixin, mixins.RetrieveModelMixin):
    def list(self, request, *args, **kwargs):
        self.serializer_class = BulletinListSerializer
        return super(BulletinCreateView, self).list(request, *args, **kwargs)

    def create(self, request, *args, **kwargs):
        self.serializer_class = BulletinCreateSerializer
        return super(BulletinCreateView, self).create(request, *args, **kwargs)

    def retrieve(self, request, *args, **kwargs):
        """ Настройка сериалайзера по URL-параметрам """
        params = self.request.query_params
        if 'fields' in params:
            self.serializer_class = BulletinFullDetailSerializer
            return super().retrieve(request, *args, **kwargs)

        self.serializer_class = BulletinDetailSerializer
        return super().retrieve(request, *args, **kwargs)

    def get_queryset(self):
        """ Сортировка объявлений по URL-параметрам """
        params = self.request.query_params
        if 'sort' in params:
            sorting_field = params['sort']
            if 'desc' in params:
                sorting_field = '-' + sorting_field
            queryset = Bulletin.objects.all().order_by(sorting_field)
            return queryset
        else:
            queryset = Bulletin.objects.all()
        return queryset
