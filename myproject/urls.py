from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from csvreader import views as csvreader_views  

urlpatterns = [
    path('admin/', admin.site.urls),
    path('csvreader/', include('csvreader.urls')),
    path('', csvreader_views.upload_file, name='home'),  
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
