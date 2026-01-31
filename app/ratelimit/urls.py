from django.urls import path
from . import views

urlpatterns = [
    path('limit/', views.getResponse, name='response'),
]