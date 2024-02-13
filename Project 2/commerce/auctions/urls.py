from django.urls import path
from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path('create/', views.create_listing, name='create_listing'),
    path('listing/<int:listing_id>/', views.listing_detail, name='listing_detail'),
    path('categories/', views.category_list, name='category_list'),
    path('categories/<str:category_name>/', views.category_view, name='category_view'),
    path('watchlist/', views.view_watchlist, name='view_watchlist'),
    path('watchlist/toggle/<int:listing_id>/', views.toggle_watchlist, name='toggle_watchlist'),
]
