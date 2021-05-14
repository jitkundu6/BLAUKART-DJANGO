
from django.urls import path, include

from . import views
from django.contrib.auth import views as auth_views

app_name = 'accounts'

urlpatterns = [
    ##### user related path ##########################
    path('signup/', views.signup, name="signup"),
    path('signuplite/', views.signuplite, name="signuplite"),
    path('login/', views.login_view, name ='login'),

    #path('logout/', auth_views.LogoutView.as_view(template_name ='user/index.html'), name ='logout'),
    #path('logout/', auth_views.LogoutView.as_view(template_name ='accounts/login.html'), name ='logout'),
    path('logout/', views.logout, name ='logout'),

    path('verify_email/', views.verify_email_view, name ='verify_email'),
    path('send_email_otp/', views.send_email_otp, name ='send_email_otp'),

    path('verify_phone/', views.verify_phone_view, name ='verify_phone'),
    path('send_phone_otp/', views.send_phone_otp, name ='send_phone_otp'),

    path('password_change/', views.password_change, name='password_change'),

    path('password_forget/', views.password_forget, name='password_forget'),
    path('password_reset_pending/', views.password_reset_pending, name='password_reset_pending'),
    path('password_reset/<str:token>/', views.password_reset_by_link, name='password_reset_by_link'),
    path('password_reset_otp/', views.password_reset_by_otp, name='password_reset_otp'),
    path('password_reset/', views.password_reset, name ='password_reset'),

    path('user_dashboard/', views.user_dashboard, name ='user_dashboard'),
    path('admin_dashboard/', views.admin_dashboard, name ='admin_dashboard'),
    
    path('user_update/', views.user_update, name ='user_update')
]

