from django.urls import path
from . import views

urlpatterns = [
        path('wiki/<str:title>/', views.entry, name='entry'),
        path("edit/<str:title>", views.edit_entry, name="edit_entry"),
        path("new", views.create_entry, name="create_entry"),
        path("random", views.random_entry, name="random_entry"),
        path('search', views.search, name='search'),
        path("", views.index, name="index")
]
