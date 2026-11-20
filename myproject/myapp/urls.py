from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('products/', views.products, name='products'),
    path('login/', views.login_page, name='login'),
    path('register/', views.register_page, name='register'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('logout/', views.logout_page, name='logout'),

    path('add-to-cart/<int:product_id>/',
         views.add_to_cart, name='add_to_cart'),

    path('order/', views.order_page, name='order'),

    path('update-cart/<int:product_id>/',
         views.update_cart, name='update_cart'),

    path('checkout/', views.checkout, name='checkout'),

    path('place-order/', views.place_order, name='place_order'),
]