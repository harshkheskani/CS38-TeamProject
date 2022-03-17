from django.urls import path
from leidos_app import views

app_name = 'leidos_app'

urlpatterns = [
	path('', views.homepage, name = 'homepage'),
	path('login/', views.user_login, name='login'),
	path('logout/', views.user_logout, name='logout'),
	path('register/', views.user_register, name='register'),
	path('profile/', views.profile, name="profile"),
	path('register_business/', views.register_business, name='register_business'),
    path('business/<slug:business_name_slug>/', views.business, name="business"),
	path('business/<slug:business_name_slug>/add_opening_hours/', views.add_opening_hours, name="add_opening_hours"),
	path('business/<slug:business_name_slug>/create_section/', views.create_section, name="create_section"),
	path('business/<slug:business_name_slug>/create_section_item/', views.create_section_item, name="create_section_item"),
	path('business/<slug:business_name_slug>/edit_business/', views.edit_business, name="edit_business"),
	path('business/<slug:business_name_slug>/save_business_edit/', views.save_business_edit, name="save_business_edit"),
	path('save_opening_hours_edit/<int:hours_pk>', views.save_opening_hours_edit, name="save_opening_hours_edit"),
	path('delete_opening_hours/<int:hours_pk>', views.delete_opening_hours, name="delete_opening_hours"),
	path('delete_section/<int:section_pk>', views.delete_section, name="delete_section"),
	path('delete_section_item/<int:item_pk>', views.delete_section_item, name="delete_section_item"),
	path('business/<slug:business_name_slug>/add_comment/', views.add_comment, name="add_comment"),
	path('delete_comment/<int:comment_pk>', views.delete_comment, name="delete_comment"),
	path('search_business/<str:path>', views.search_business, name="search_business"),
	path('add_favorite/<slug:business_name_slug>', views.add_favorite, name="add_favorite"),
	path('remove_favorite/<slug:business_name_slug>', views.remove_favorite, name="remove_favorite"),
	path('prof_pic_edit', views.save_profile_pic, name="save_profile_pic"),
	path('prof_desc_edit', views.save_profile_desc, name="save_profile_desc"),
]