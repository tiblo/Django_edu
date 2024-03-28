from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('', views.index, name='index'),
    path('testing', views.testing, name='testing'),
    path('somepage', views.somepage, name='somepage'),
    path('write', views.write, name='write'),
    path('update/<int:id>', views.update, name='update'),
    path('delete/<int:id>', views.delete, name='delete'),
]
