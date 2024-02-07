from django.urls import path
from . import views

urlpatterns = [
        path('wiki/<str:title>/', views.entry, name='entry'),
        path('search', views.search, name='search'),
        path("", views.index, name="index")
]
