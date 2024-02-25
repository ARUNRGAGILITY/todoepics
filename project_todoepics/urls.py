from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static 

urlpatterns = [
    path('admin/', admin.site.urls),
    
    # web for web pages: urls
    path('', include('app_web.urls')),
    # LoginSystem
    path('loginsys/', include('app_loginsystem.urls')),
    # TodoEpics
    path('todoepics/', include('app_todoepics.urls')),
    
    # markdown
    path('markdownx/', include('markdownx.urls')), 
]
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)