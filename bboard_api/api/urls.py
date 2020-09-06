from django.urls import path, include
from rest_framework import routers

from .views import *


router = routers.DefaultRouter()
router.register('bulletins', BulletinsView, basename='bulletins')

app_name = 'api'
urlpatterns = [
    path('', include((router.urls, 'api'))),
]

