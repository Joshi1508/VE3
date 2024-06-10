from django.urls import path
from . import views

urlpatterns = [
    path('upload/', views.upload_file, name='upload_file'), 
    path('success/', views.success, name='success'),
     path('visualize/<path:file_path>/', views.data_visualization, name='data_visualization'),

]
