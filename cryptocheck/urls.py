from django.urls import path
from . import views #import views.py


urlpatterns = [
    path('', views.index, name="cryptocheck-home"),
    path('getCMCdata/<str:coinRankID>/', views.getCMCdata, name="getCMCdata"),
]
