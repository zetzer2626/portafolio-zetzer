from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('about/', views.about, name='about'),
    path('profile/', views.ProfileDetailView.as_view(), name='profile_detail'),
    path('profile/edit/', views.ProfileUpdateView.as_view(), name='profile_update'),
    path('experience/create/', views.experience_create, name='experience_create'),
    path('experience/<int:pk>/edit/', views.experience_update, name='experience_update'),
    path('experience/<int:pk>/delete/', views.experience_delete, name='experience_delete'),
    path('certification/create/', views.certification_create, name='certification_create'),
    path('certification/<int:pk>/edit/', views.certification_update, name='certification_update'),
    path('certification/<int:pk>/delete/', views.certification_delete, name='certification_delete'),
] 