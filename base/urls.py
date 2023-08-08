from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('',views.index,name='index'),
    path('product/<int:pk>',views.product,name='product'),
    path('products/product/<int:pk>',views.product,name='product'),
    path('products/',views.all_products,name='all_products'),
    path('register/',views.register,name='register'),
    path('login/',views.login_page,name='login_page'),
    path('logout/',views.logout_page,name='logout'),
    path('cart/',views.item_cart,name='cart'),
    path('add_to_cart/<int:id>',views.add_to_cart,name='add_to_cart'),
    path('remove_from_cart/<int:id>',views.remove_from_cart,name='remove_from_cart')
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
