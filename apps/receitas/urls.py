from django.urls import path
from .views import *

urlpatterns = [
    path('', index, name='index'),
    path('receita/<int:receita_id>', receita, name='receita'),
    path('buscar', busca, name='buscar'),
    path('criar/receita', cria_receita, name='cria_receita'),
    path('deleta/<int:receita_id>', deleta_receita, name='deleta_receita'),
    path('edita/<int:receita_id>', edita_receita, name='edita_receita'),
]
