from django.urls import path
from leidos_app import views

app_name = 'leidos_app'

urlpatterns = [
	path('', views.base, name='base'),
	path('homepage/', views.homepage, name = 'homepage'),
	path('login/', views.user_login, name='login'),
	path('logout/', views.user_logout, name='logout'),
	path('register/', views.user_register, name='register'),
	path('create_menu/', views.create_menu, name ='create_menu'),
	path('menu/', views.menu, name="menu"),
    path('business/', views.business, name="business"),


	
]