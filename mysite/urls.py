from django.contrib import admin
from django.urls import path, include
from django.contrib.auth import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/login/', views.login, name='login'),
    path('accounts/logout/', views.logout, name='logout', kwargs={'next_page': '/'}), # 追加
    path('', include('demo_app.urls')),

]
