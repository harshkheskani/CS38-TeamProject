from django.urls import path
from leidos_app import views

app_name = 'leidos_app'

urlpatterns = [
	path('', views.base, name='base'),

	path('login/', views.login, name='login'),
	path('register/', views.register, name='register'),
	path('create_menu/', views.create_menu, name ='create_menu'),
	path('menu/', views.menu, name="menu"),


	
]