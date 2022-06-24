from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib import auth, messages
from apps.receitas.models import Receita

# Create your views here.


def cadastro(request):
    """Cadastra uma nova pessoa no sistema"""
    if request.method == 'POST':
        nome = request.POST['nome']
        email = request.POST['email']
        senha = request.POST['password']
        senha2 = request.POST['password2']

        if campo_vazio(nome):
            messages.error(request, "O nome não pode ficar em branco")
            return redirect('cadastro')
        if campo_vazio(email):
            messages.error(request, "O email não pode ficar em branco")
            return redirect('cadastro')
        if senha != senha2:
            messages.error(request, 'As senhas não são iguais')
            print("Confirmação de senha errada")
            return redirect('cadastro')
        if User.objects.filter(email=email).exists():
            messages.error(request, 'Este email já está cadastrado')
            print("Usuário já cadastrado")
            return redirect('cadastro')
        if User.objects.filter(username=nome).exists():
            messages.error(request, 'Este usuário já está cadastrado')
            print("Usuário já cadastrado")
            return redirect('cadastro')
        user = User.objects.create_user(username=nome, email=email, password=senha)
        user.save()
        print("Usuário cadastrado com sucesso")
        messages.success(request, 'Cadastro realizado com sucesso')
        return redirect('login')

    elif request.method == 'GET':
        return render(request, 'usuarios/cadastro.html')


def login(request):
    if request.method == 'POST':
        email = request.POST['email']
        senha = request.POST['password']

        if User.objects.filter(email=email).exists():
            nome = User.objects.filter(email=email).values_list('username', flat=True).get()
            user = auth.authenticate(request, username=nome, password=senha)
            if user is not None:
                auth.login(request, user)
                print("Login realizado com sucesso")
                return redirect('dashboard')

        return redirect('login')

    elif request.method == 'GET':
        return render(request, 'usuarios/login.html')


def logout(request):
    auth.logout(request)
    return redirect('index')


def dashboard(request):
    if request.user.is_authenticated:

        receitas_do_usuario = Receita.objects.filter(pessoa=request.user.id).order_by('-data_receita')
        dados = {
            'receitas': receitas_do_usuario
        }

        return render(request, 'usuarios/dashboard.html', dados)
    else:
        return redirect('index')


def campo_vazio(campo):
    return not campo.strip()
