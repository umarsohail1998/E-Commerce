from app.forms import LoginForm,MyPasswordChangeForm, MyPasswordResetForm, MySetPasswordForm
from app.models import Product
from django.urls import path
from app import views
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth import authenticate, views as auth_views 
urlpatterns = [
    path('',views.ProductView.as_view(), name='home'),
    path('product-detail/<int:pk> ', views.ProductDetailView.as_view(), name='product-detail'),    
    path('add-to-cart/', views.add_to_cart, name='add-to-cart'),
    path('cart/', views.show_cart, name='showcart'),
    path('pluscart/', views.plus_cart),
    path('minuscart/', views.minus_cart),
    path('removecart/', views.remove_cart),
    path('buy/', views.buy_now,  name='buy-now'),
    path('profile/', views.ProfileView, name='profile'),
    path('address/', views.address, name='address'),
    path('orders/', views.orders, name='orders'),
    path('category/<int:num>', views.category, name='category'),
    path('contectus/', views.contectus, name='contectus'),
    path('createuser/',views.CustomerRegistrationView, name= 'signup' ),
    path('userlogin/',views.userLogin,name= 'userlogin' ),
    path('userlogout/',views.userLogout,name= 'logout' ),
    path('search/',views.search,name= 'search' ),
    path('passwordchange/', auth_views.PasswordChangeView.as_view(template_name= 'app/passwordchange.html', form_class = MyPasswordChangeForm),name= 'passwordchange'),
    path('password-reset/', auth_views.PasswordResetView.as_view(template_name='app/password_reset.html', form_class= MyPasswordResetForm) , name= 'password_reset'),
    path('password-reset/done/', auth_views.PasswordResetDoneView.as_view(template_name='app/password_reset_done.html') , name= 'password_reset_done'),
    path('password-reset-confirm/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(template_name='app/password_reset_confirm.html',  form_class = MySetPasswordForm) , name= 'password_reset_confirm'),
    path('password-reset-complete/', auth_views.PasswordResetCompleteView.as_view(template_name='app/password_reset_complete.html') , name= 'password_reset_complete'),
    path('checkout/', views.checkout, name='checkout'),
    path('paymentdone/', views.payment_done, name='paymentdone'),  


    path('discount',views.discount,name='discount'),
    path('account',views.account,name='account')  
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
