from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('register/', views.register_asset, name='register_asset'),
    path('assets/', views.assets_list, name='assets_list'),
    path('delete_asset/<int:asset_id>/', views.delete_asset, name='delete_asset'),
    path('rent_asset/<int:asset_id>/', views.rent_asset, name='rent_asset'),
    path('dashboard/', views.user_dashboard, name='dashboard'),
]


