from django.contrib import admin
from django.urls import path
from . import views
from django.contrib.auth import views as auth_views  # for logout

urlpatterns = [
    # 🧭 Admin Panel
    path('admin/', admin.site.urls),

    # 🧾 Authentication
    path('', views.loginn, name="home"),                # default page = login
    path('registr/', views.registr, name="registr"),
    path('registeruser/', views.registeruser, name="registeruser"),
    path('loginn/', views.loginn, name="loginn"),
    path('loginform/', views.loginform, name="loginform"),
    path('logout/', auth_views.LogoutView.as_view(next_page='/loginn/'), name='logout'),

    # 🧍‍♀️ Employee Panel
    path('index/', views.index, name="index"),

    # 🕒 Attendance System
    path('punch/', views.punch, name="punch"),
    path('attendance-report/', views.attendance_report, name="attendance_report"),
    path('change-password/', views.change_password, name='change_password'),
]
