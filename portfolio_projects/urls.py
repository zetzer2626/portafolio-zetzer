from django.urls import path
from . import views

urlpatterns = [
    path('', views.ProjectListView.as_view(), name='project_list'),
    path('create/', views.ProjectCreateView.as_view(), name='project_create'),
    path('category/<slug:slug>/', views.category_projects, name='category_projects'),
    path('<int:project_id>/comment/', views.add_comment, name='add_comment'),
    path('<int:project_id>/vote/', views.vote_project, name='vote_project'),
    path('<slug:slug>/edit/', views.ProjectUpdateView.as_view(), name='project_update'),
    path('<slug:slug>/delete/', views.ProjectDeleteView.as_view(), name='project_delete'),
    path('<slug:slug>/images/', views.project_images, name='project_images'),
    path('<slug:slug>/images/<int:image_id>/edit/', views.project_image_update, name='project_image_update'),
    path('<slug:slug>/images/<int:image_id>/delete/', views.project_image_delete, name='project_image_delete'),
    path('<slug:slug>/', views.ProjectDetailView.as_view(), name='project_detail'),
] 