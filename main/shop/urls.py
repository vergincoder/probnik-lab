from django.urls import path
from . import views

urlpatterns = [
    path('sign-up', views.sign_up),
    path('sign-in', views.sign_in),
    path('sign-out', views.sign_out),



    path('cart', views.cart_view),

    path('product/<int:pk>', views.product_detail),
    path('product', views.product_add),
    path('products', views.product_view),
]
