from django.urls import path
from . import views

urlpatterns = [
    path('', views.index),
    path('add/', views.add_contact),
    path('edit/<str:contact_id>/', views.edit_contact),
    path('delete/<str:contact_id>/', views.delete_contact),
    path('search/', views.search_contact),
    path('emergency/', views.emergency),
    path('frequent/', views.frequent),
    path('favorites/', views.favorites),
    path('relationship/', views.relationship),
    path('export/', views.export_contacts),
]
