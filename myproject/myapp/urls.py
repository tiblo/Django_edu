from django.urls import path
from . import views

urlpatterns = [
    #path('', views.first, name='first'),
    path('', views.index, name='index'),
    path('write', views.write, name='write'),
    # path('update', views.update, name='update'), # query parameter
    path('update/<int:id>', views.update, name='update'), # path parameter
    path('delete/<int:id>', views.delete, name='delete'),
]
