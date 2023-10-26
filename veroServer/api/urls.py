from django.urls import path
from . import views

urlpatterns=[
    #path('', views.getData),
    path('api/upload-vehicles/', views.upload_vehicles, name='upload-vehicles'),
]