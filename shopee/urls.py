# urls.py

from django.urls import path
from django.contrib.auth import views as auth_views
from . import views


urlpatterns = [
    path('', views.index, name='index'),
    path('products/', views.product_list, name='product_list'),
    path('products/<int:product_id>/', views.product_detail, name='product_detail'),
    path('cart/', views.cart_view, name='cart_view'),
    path('user/', views.user_detail, name='user_detail'),
    path('add-to-cart/', views.add_to_cart, name='add_to_cart'),
    path('update-cart/', views.update_cart, name='update_cart'),
    path('login_register/', views.login_register, name='login_register'),
    path('login/', views.login_view, name='login_user'),
    path('register/', views.register_view, name='register_user'),
    path('update-user-info/', views.update_user_info, name="update_user_info"),
    path('add_address/', views.add_address, name='add_address'),
    path('logout/', auth_views.LogoutView.as_view(next_page='login_user'), name='logout'),
    path('purchase/', views.purchase, name='purchase'),
     path('products/', views.product_list, name='product_list'),
    path('create-admin/', views.create_admin_user),
     

]

