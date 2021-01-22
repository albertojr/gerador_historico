
from django.contrib import admin
from django.urls import path

urlpatterns = [
    path('', admin.site.urls),
]

admin.site.site_header = 'Gerador de Históricos'
admin.autodiscover()
admin.site.enable_nav_sidebar = False
