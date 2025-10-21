from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.shortcuts import render
def home(request):
    return render(request, 'home.html')
urlpatterns = [
    path('admin/', admin.site.urls),
    path('', home, name='home'),
    path('accounts/', include('accounts.urls')),
    path('appointments/', include('appointments.urls')),
    path('accessories/', include('accessories.urls')),
    path('reminders/', include('medicine_reminders.urls')),  # Keep the URL path as 'reminders/' but include from 'medicine_reminders'
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
