from django.urls import path
from leidos_app import views

app_name = 'leidos_app'

urlpatterns = [
	path('', views.base, name='base'),

	path('login/', views.login, name='login'),
	path('register/', views.register, name='register'),
	
]