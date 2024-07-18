from django.urls import path
from . import views

urlpatterns = [
    path("login/", views.login_view, name="login"),
    path('dashboard/', views.dashboard, name='dashboard'),
    path("logout/", views.logout_user, name="logout_user"),
    path('getdata/<int:pk>/',views.get_data,name="getdata"),

]