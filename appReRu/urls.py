from django.urls import path
from .views import *


urlpatterns = [
    path('register/', register, name='register'),
    path('login/', login_user, name='login_user'),
    path('logout/', logout_user, name='logout_user'),
    path('cart/', cart, name='cart'),
    path('checkout/', checkout, name='checkout'),
    path('contact/', contact, name='contact'),
    path('shop_detail/<int:pk>/', shop_detail, name='shop_detail'),
    path('', shop, name='shop'),
    path('error/', error, name='error'),
	path('update_item/', updateItem, name="update_item"),
	path('process_order/', processOrder, name="process_order"),
    path('search/', search_view, name='search'),
    path('Account_User/', Account_User, name='acc'),
    path('user/profile/', User_Profile, name='user_profile'),
    path('refunds/<str:pk>/', refund_request, name='refund_request'),
    path('inbox/', inbox, name='inbox'),
]