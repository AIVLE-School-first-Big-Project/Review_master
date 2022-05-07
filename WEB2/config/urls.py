from django.contrib import admin
from django.urls import path
from django.conf.urls import include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('app/', include('homeapp.urls')),
    path('/', include('homeapp.urls')),
    path('app/analysis/', include('analysisapp.urls', namespace='analysis')),
    path('app/account/', include('accountapp.urls', namespace='account')),
    path('app/board/', include('board.urls', namespace='board')),
]

urlpatterns += \
    static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
