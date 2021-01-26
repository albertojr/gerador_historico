
from historico import views
from django.urls import path

urlpatterns = [
    path('lista/alunos/json',views.historicos_json,name='historicos_json'),
    path('historico',views.historico,name='historico')

]