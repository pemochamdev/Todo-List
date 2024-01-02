from django.urls import path

from todoapp import views

urlpatterns = [
    path('', views.home, name='home'),
    path('delete-task/<id>/', views.delete_task, name='delete_task'),
    path('update/<id>/', views.update, name='update'),
    path('register/', views.register, name='register'),
    path('login/', views.CustomLoginView.as_view(), name='login'),
    path('logout/', views.CustomLogoutView.as_view(), name='logout'),
]
