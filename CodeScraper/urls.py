from django.urls import path
from . import views

urlpatterns=[
  path('', views.index, name='index'),
  path('process',views.process, name='process'),
  path('result/<lang>/<q_id>', views.result, name='result')
]