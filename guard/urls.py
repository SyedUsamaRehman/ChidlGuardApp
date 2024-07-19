from django.urls import path
from . import views

urlpatterns = [
    path("", views.login_view, name="login"),
    path('dashboard/', views.dashboard, name='dashboard'),
    path("logout/", views.logout_user, name="logout_user"),
    path('getdata/<int:pk>/',views.get_data,name="getdata"),
    path('check-abnormal-values/<int:pk>/<str:graph_name>/', views.check_abnormal_values, name='check_abnormal_values'),

]