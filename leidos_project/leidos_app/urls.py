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
    path('business/<slug:business_name_slug>/', views.business, name="business"),
	path('business/<slug:business_name_slug>/add_hours/', views.add_opening_hours, name="add_hours"),
	path('business/<slug:business_name_slug>/edit_business/', views.edit_business, name="edit_business")
]