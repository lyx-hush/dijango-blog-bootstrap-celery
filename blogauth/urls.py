from django.urls import path
from . import views

app_name = 'blogauth'
urlpatterns = [
    path('login', views.mylogin, name='login'),
    path('register', views.register, name='register'),
    path('captcha', views.send_email_captcha, name='captcha'),
    path('logout', views.mylogout, name='logout')
]
