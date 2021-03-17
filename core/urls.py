
from django.conf.urls import url, include
from django.contrib import admin
from django.urls import path
from historico import views
from django.contrib.auth import views as auth_views

# from django.contrib.auth import views as auth_views


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.home_geral,name='home_geral'),
    path('historicos/', include('historico.urls')),
    path("select2/", include("django_select2.urls")),
]

admin.site.site_header = 'Gerador de Históricos'
admin.site.index_title = 'Features area'                 # default: "Site administration"
admin.site.site_title = 'Login - Gerador de histórico' # default: "Django site admin"

admin.autodiscover()
admin.site.enable_nav_sidebar = False
