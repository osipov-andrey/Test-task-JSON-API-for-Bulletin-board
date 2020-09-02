from rest_framework import generics

from .models import Bulletin
from .serializers import BulletinDetailSerializer, BulletinListSerializer


class BulletinCreateView(generics.CreateAPIView):
    serializer_class = BulletinDetailSerializer


class BulletinsListView(generics.ListAPIView):
    serializer_class = BulletinListSerializer

    def get_queryset(self):
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


class BulletinDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = BulletinDetailSerializer
    queryset = Bulletin.objects.all()