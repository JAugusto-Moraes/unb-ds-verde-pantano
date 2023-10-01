from django.urls import path
from inicial.views import index, locais_de_atendimento

urlpatterns = [
    path('', index, name='index'),
    path("atendimento", locais_de_atendimento, name='locais_de_atendimento')
]
