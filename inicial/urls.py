from django.urls import path
from inicial.views import *

urlpatterns = [
    path('', index, name='index'),
    path("atendimento", locais_de_atendimento, name='locais_de_atendimento'),
    path("atendimento/", buscar, name='buscar'),
    path("informacoes/<int:hospital_cnes>", mais_informacoes, name='mais_informacoes'),
    path("avaliar/<int:hospital_cnes>", avaliar_hospital, name='avaliar_hospital'),
    path("duvidas_frequentes", duvidas_frequentes, name='duvidas_frequentes'),
    path("sobrenos", sobre_nos, name="sobre_nos"),
    path("cadastro", cadastro, name='cadastro'),
    path("login/<str:view_name>", login_site, name='login'),
    path("login/confirmacao/<str:view_name>", confirma_email, name="confirma_email"),
    path("logout", logout_site, name="logout"),
    path("redefinir_senha/<str:username>/<str:token>", redefinir_senha, name="redefinir_senha"),
    path("perfil/avaliacoes", minhas_avaliacoes, name="minhas_avaliacoes"),
    path("perfil/avaliacoes/", pesquisar_avaliacoes, name="pesquisar_avaliacoes"),
    path("perfil/avaliacoes/<int:avaliacao_id>", avaliacao_completa, name="avaliacao_completa"),
    path("perfil/meus_dados", meus_dados, name="meus_dados"),
    path("perfil/editar_dados", editar_dados, name="editar_dados"),
    path("triagem", triagem, name="triagem"),
    path("triagem/a1",adulto1, name="adulto1"),
    path("triagem/a2",adulto2, name="adulto2"),
    path("triagem/a3",adulto3, name="adulto3"),
    path("triagem/a4",adulto4, name="adulto4"),
    path("triagem/b1",crianca1, name="crianca1"),
    path("triagem/b2",crianca2, name="crianca2"),
    path("triagem/b3",crianca3, name="crianca3"),
    path("triagem/b4",crianca4, name="crianca4"),
    path("resultado_vermelho",resultado_vermelho, name="resultado_vermelho"),
    path("resultado_laranja",resultado_laranja, name="resultado_laranja"),
    path("resultado_amarelo",resultado_amarelo, name="resultado_amarelo"),
    path("resultado_verde",resultado_verde, name="resultado_verde"),
    path("resultado_azul",resultado_azul, name="resultado_azul"),
]
