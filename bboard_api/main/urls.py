from django.urls import path

from .views import *


app_name = 'main'
urlpatterns = [
    path('api/bulletin/<int:pk>/', BulletinDetailView.as_view(), name='bulletin'),
    path('api/bulletin/create/', BulletinCreateView.as_view(), name='create'),
    path('api/bulletins/', BulletinsListView.as_view(), name='bulletins'),
]
