from django.urls import include, path
from django.contrib import admin
import xpload


api_urls = [
    path('cdb_rest/', include('cdb_rest.urls')),
    path('cdb_rest/', include('xpload.urls'))
]

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include(api_urls)),
    path('rds/', include(xpload.urls.rds))
]
