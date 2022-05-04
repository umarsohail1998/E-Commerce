from app.forms import LoginForm,MyPasswordChangeForm, MyPasswordResetForm, MySetPasswordForm
from app.models import Product
from django.urls import path
from analysis import views
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth import authenticate, views as auth_views 

urlpatterns = [
    path('', views.index, name='index'),
    path('user_login/', views.user_login, name ='user_login'),
    path('order_placed/', views.order_placed, name ='order_placed'),
    path('Customers/', views.Customers, name ='Customers'),
    path('Products/', views.Products, name ='Products'),
    path('log_out/', views.log_out, name ='log_out'),
    
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
