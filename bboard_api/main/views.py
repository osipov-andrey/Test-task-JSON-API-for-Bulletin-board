from rest_framework import generics

from .serializers import *


class BulletinCreateView(generics.CreateAPIView):
    """ Создать объявление """
    serializer_class = BulletinCreateSerializer


class BulletinsListView(generics.ListAPIView):
    """ Получить все объявления """
    serializer_class = BulletinListSerializer

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


class BulletinDetailView(generics.RetrieveAPIView):
    """ Получить одно объявление """
    serializer_class = BulletinDetailSerializer
    queryset = Bulletin.objects.all()

    def dispatch(self, request, *args, **kwargs):
        """ Настройка сериалайзера по URL-параметрам """
        response = super().dispatch(request, *args, **kwargs)
        params = self.request.query_params
        if 'fields' in params:
            self.serializer_class = BulletinFullDetailSerializer
            response = super().dispatch(request, *args, **kwargs)
        return response
