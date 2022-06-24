from apps.receitas.models import Receita
from django.shortcuts import render


def busca(request):
    lista_receitas = Receita.objects.order_by('-data_receita').filter(publicada=True)

    if 'buscar' in request.GET:
        buscar_receita = request.GET['buscar']
        if buscar_receita:
            lista_receitas = lista_receitas.filter(nome_receita__icontains=buscar_receita)

    dados = {
        'receitas': lista_receitas
    }

    return render(request, 'receitas/buscar.html', dados)
