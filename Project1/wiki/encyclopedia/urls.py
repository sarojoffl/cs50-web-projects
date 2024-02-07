from django.urls import path
from . import views

urlpatterns = [
        path('wiki/<str:title>/', views.entry, name='entry'),
        path("new", views.create_entry, name="create_entry"),
        path('search', views.search, name='search'),
        path("", views.index, name="index")
]
