from django.urls import path
from leidos_app import views

app_name = 'leidos_app'

urlpatterns = [
	path('', views.base, name='base'),
	path('homepage/', views.homepage, name = 'homepage'),
	path('login/', views.user_login, name='login'),
	path('logout/', views.user_logout, name='logout'),
	path('register/', views.user_register, name='register'),
	path('register_business/', views.register_business, name='register_business'),
	path('menu/', views.menu, name="menu"),
    path('business/<slug:business_name_slug>/', views.business, name="business"),
	path('business/<slug:business_name_slug>/add_hours/', views.add_opening_hours, name="add_hours"),
	path('business/<slug:business_name_slug>/edit_business/', views.edit_business, name="edit_business"),
	path('business/<slug:business_name_slug>/save_business_edit/', views.save_business_edit, name="save_business_edit"),
	path('save_opening_hours_edit/<int:hours_pk>', views.save_opening_hours_edit, name="save_opening_hours_edit"),
]