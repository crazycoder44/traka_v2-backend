from django.urls import path

from . import views

urlpatterns = [
    path('register/', views.users_register_view),
    path('login/', views.user_login_view),
    path('token/refresh/', views.token_refresh_view),
    
    path('products/', views.products_list_create_view),
    path('products/<int:id>/update/', views.products_update_view),
    path('products/<int:pk>/delete/', views.products_destroy_view),
    path('products/<int:pk>/', views.products_detail_view),

    path('branches/', views.branches_listcreate_view),
    path('branches/<int:pk>/update/', views.branches_update_view),
    path('branches/<int:pk>/delete/', views.branches_destroy_view),
    path('branches/<int:id>/', views.branches_detail_view),

    path('users/', views.users_list_view),
    path('users/<int:pk>/update/', views.users_update_view),
    path('users/<int:pk>/delete/', views.users_destroy_view),
    path('users/<int:pk>/', views.users_detail_view, name='users_detail_view'),

    path('sales/', views.sales_listcreate_view),
    # path('sales/<int:pk>/update/', views.sales_update_view),
    path('sales/<int:pk>/delete/', views.sales_destroy_view),
    path('sales/<int:pk>/', views.sales_detail_view),

    path('returns/', views.returns_listcreate_view),
    # path('returns/<int:pk>/update/', views.returns_update_view),
    path('returns/<int:pk>/delete/', views.returns_destroy_view),
    path('returns/<int:pk>/', views.returns_detail_view),
    
    path('inventory/', views.inventory_listcreate_view),
    path('inventory/<int:pk>/delete/', views.inventory_destroy_view),
    path('inventory/<int:pk>/', views.inventory_detail_view)
]