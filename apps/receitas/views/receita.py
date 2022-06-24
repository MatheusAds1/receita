from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.models import User
from django.contrib import messages
from apps.receitas.models import Receita
from django.core.paginator import Paginator


# Create your views here.
# O contexto passado para o render(dados) deve ser um dict


def index(request):
    """Renderiza a página inicial"""
    # receitas = Receita.objects.all()
    receitas = Receita.objects.order_by('-data_receita').filter(publicada=True)
    paginator = Paginator(receitas, 6)
    page = request.GET.get('page')
    receitas_por_pagina = paginator.get_page(page)

    dados = {
        'receitas': receitas_por_pagina
    }

    return render(request, 'receitas/index.html', dados)


def receita(request, receita_id):
    """Renderiza uma página com os dados de uma receita"""
    receita_obj = get_object_or_404(Receita, pk=receita_id)
    receita_dict = {'receita': receita_obj}

    return render(request, 'receitas/receita.html', receita_dict)


def cria_receita(request):
    """Cria uma receita e redireciona para a dasboard se o usuário estiver logado"""
    if request.user.is_authenticated:
        if request.method == 'POST':
            nome_receita = request.POST['nome_receita']
            ingredientes = request.POST['ingredientes']
            modo_preparo = request.POST['modo_preparo']
            tempo_preparo = request.POST['tempo_preparo']
            rendimento = request.POST['rendimento']
            categoria = request.POST['categoria']
            foto = request.FILES['foto_receita']
            user = get_object_or_404(User, pk=request.user.id)
            receita = Receita.objects.create(pessoa=user, nome_receita=nome_receita, ingredientes=ingredientes,
                                             modo_preparo=modo_preparo, tempo_preparo=tempo_preparo,
                                             rendimento=rendimento, categoria=categoria, foto_receita=foto)
            receita.save()
            return redirect('dashboard')

        else:
            return render(request, 'receitas/cria_receita.html')
    else:
        return redirect('login')


def deleta_receita(request, receita_id):
    """Deleta uma receita e redireciona para a dashboard"""
    receita = get_object_or_404(Receita, pk=receita_id)
    receita.delete()
    messages.success(request, 'Receita deletada com sucesso')
    return redirect('dashboard')


def edita_receita(request, receita_id):
    """Edita uma receita e redireciona para a dashboard"""
    if request.method == 'POST':
        receita = Receita.objects.get(pk=receita_id)
        receita.nome_receita = request.POST['nome_receita']
        receita.ingredientes = request.POST['ingredientes']
        receita.modo_preparo = request.POST['modo_preparo']
        receita.tempo_preparo = request.POST['tempo_preparo']
        receita.rendimento = request.POST['rendimento']
        receita.categoria = request.POST['categoria']
        if 'foto_receita' in request.FILES:
            receita.foto_receita = request.FILES['foto_receita']
        # foto = request.FILES.get('foto_receita', '')
        # if foto:
        #     receita.foto_receita = foto

        # user = get_object_or_404(User, pk=request.user.id)
        receita.save()
        messages.success(request, 'Receita atualizada com sucesso')
        return redirect('dashboard')
    else:
        receita = get_object_or_404(Receita, pk=receita_id)
        receita_a_editar = {'receita': receita}
        return render(request, 'receitas/edita_receita.html', receita_a_editar)