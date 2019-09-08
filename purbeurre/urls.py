from django.contrib import admin
from django.urls import path, include

from index.views import index

urlpatterns = [
    path('admin/', admin.site.urls),
    path('account/', include('account.urls')),
    path('index/', include('index.urls')),
    path('aliments/', include('aliments.urls')),
    path('', index, name='start')
]
