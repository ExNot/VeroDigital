from django.urls import path
from .views import upload_csv
from . import views

urlpatterns=[
    #path('', views.getData),
    path('upload/', upload_csv, name='upload_csv'),
]