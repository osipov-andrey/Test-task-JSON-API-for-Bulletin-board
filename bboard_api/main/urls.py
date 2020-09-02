from django.urls import path, include

from .views import *


app_name = 'main'
urlpatterns = [
    path('api/bulletin/<int:pk>/', BulletinDetailView.as_view()),
    path('api/bulletin/create/', BulletinCreateView.as_view()),
    path('api/bulletins/', BulletinsListView.as_view(), name='bulletins'),
]
