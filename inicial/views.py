from django.shortcuts import render, get_object_or_404, redirect
from django.core.mail import send_mail
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.views.decorators.csrf import csrf_exempt
from datetime import datetime
import json
from setup import settings
from .models import *
from .forms import *

def index(request):
    hospitais = Hospital.objects.order_by("-nota")[:3]
    buscar2 = BuscarForms()
    filter_form = FilterForms()
    counter = (1, 2, 3, 4, 5)
    context = {"hospitais": hospitais, "buscar": buscar2, "filter":filter_form, "counter":counter}

    return render(request, 'inicial/index.html', context)

def locais_de_atendimento(request):
    hospitais = Hospital.objects.order_by("nome")
    buscar2 = BuscarForms()
    filter_form = FilterForms()
    context = {"hospitais": hospitais, "buscar": buscar2, "filter":filter_form}

    return render(request, 'inicial/locaisdeatendimento.html', context)

def buscar(request):
    hospitais = Hospital.objects.order_by("nome")
    buscar2 = BuscarForms()
    filter_form = FilterForms()

    if "uf" in request.GET:
        uf_a_buscar = request.GET['uf']

        if uf_a_buscar:
            hospitais = hospitais.filter(uf__iexact=uf_a_buscar)

    if "municipio" in request.GET:
        municipio_a_buscar = request.GET['municipio']

        if municipio_a_buscar:
            hospitais = hospitais.filter(municipio__iexact=municipio_a_buscar)

    if "categoria" in request.GET:
        categoria_a_buscar = request.GET['categoria']

        if categoria_a_buscar:
            hospitais = hospitais.filter(categoria__iexact=categoria_a_buscar)

    if "buscar" in request.GET:
        nome_a_buscar = request.GET['buscar']

        if nome_a_buscar:
            hospitais = hospitais.filter(nome__icontains=nome_a_buscar)

    context = {"hospitais": hospitais, "buscar": buscar2, "filter":filter_form}

    return render(request, "inicial/buscar.html", context)

def mais_informacoes(request, hospital_cnes):
    hospital = get_object_or_404(Hospital, pk=hospital_cnes)
    buscar2 = BuscarForms()
    filter_form = FilterForms()
    counter = (1, 2, 3, 4, 5)
    context = {"hospital": hospital, "buscar": buscar2, "filter":filter_form, "counter":counter}

    return render(request, "inicial/maisinformacoes.html", context)

def avaliar_hospital(request, hospital_cnes):

    if not request.user.is_authenticated:
        messages.error(request, "Usuário precisa estar autenticado para avaliar hospitais")
        return redirect('mais_informacoes', hospital_cnes)

    hospital = get_object_or_404(Hospital, pk=hospital_cnes)
    buscar2 = BuscarForms()
    filter_form = FilterForms()
    context = {"hospital": hospital, "buscar": buscar2, "filter":filter_form}

    if request.method == "POST":
        numero = Avaliacao.objects.filter(usuario=request.user.username).count() + 1
        risco = request.POST["risco"]
        horario_entrada = datetime.strptime(request.POST["horario_entrada"],"%Y-%m-%dT%H:%M")
        horario_atendimento = datetime.strptime(request.POST["horario_atendimento"],"%Y-%m-%dT%H:%M")
        horario_saida = datetime.strptime(request.POST["horario_saida"],"%Y-%m-%dT%H:%M")
        duracao = horario_atendimento - horario_entrada
        avaliacao = request.POST["avaliacao"]
        observacao = request.POST["observacao"]

        Avaliacao.objects.create(
            numero=numero,
            usuario=request.user.username,
            hospital=hospital,
            risco=risco,
            horario_entrada=horario_entrada,
            horario_atendimento=horario_atendimento,
            horario_saida=horario_saida,
            duracao=duracao,
            avaliacao=avaliacao,
            observacao=observacao
        )

        return redirect('mais_informacoes', hospital_cnes)

    return render(request, "inicial/avaliarhospital.html", context)

def duvidas_frequentes(request):
    buscar2 = BuscarForms()
    filter_form = FilterForms()
    context = {"buscar": buscar2, "filter":filter_form}

    return render(request, 'inicial/duvidas_frequentes.html', context)

def cadastro(request):

    cadastro = CadastroForms()

    if request.method == "POST":
        cadastro = CadastroForms(request.POST)

        if cadastro.is_valid():
            if cadastro["senha_1"].value() != cadastro["senha_2"].value():
                messages.error(request, "Digite senhas iguais para concluir o cadastro")
                return redirect('cadastro')

            nome = cadastro["nome_cadastro"].value()
            email = cadastro["email"].value()
            senha = cadastro["senha_1"].value()

            if User.objects.filter(username=nome).exists():
                messages.error(request, "Usuário já existente")
                return redirect('cadastro')

            usuario = User.objects.create_user(
                username=nome,
                email=email,
                password=senha
            )

            usuario.save()
            messages.success(request, "Usuário cadastrado com sucesso!")
            return redirect('index')

    context = {"cadastro":cadastro}

    return render(request, 'inicial/criar_conta.html', context)

def login_site(request, view_name):
    if request.method == "POST":
        usuario = request.POST["usuario"]
        senha = request.POST["senha"]

        user = authenticate(request, username=usuario, password=senha)

        if user is not None:
            login(request, user)
            messages.success(request, f"{usuario} autenticado com sucesso!")
            return redirect(view_name)

        else:
            messages.error(request, "Usuário ou senha incorretos")
            return redirect(view_name)

def confirma_email(request, view_name):

    if request.method == "POST":
        email = request.POST["email"]

        if User.objects.filter(email__exact=email).exists():

            gerador = PasswordResetTokenGenerator()
            usuario = User.objects.get(email=email)
            token = gerador.make_token(usuario)
            username = usuario.username
            context = {"token":token, "username": username}
            # print(gerador.check_token(usuario, token))

            send_mail(
                "Redefinição de Senha",
                message=
                "Uma requisição de redefinição de senha foi feita no site MedConnect para a conta vinculada a este email, "
                f"para prosseguir com a redefinição basta acessar o seguinte link: http://127.0.0.1:8000/redefinir_senha/{username}/{token}. "
                "Caso a requisição não tenha sido feita por você por favor ignore este email.",
                from_email=settings.EMAIL_HOST_USER,
                recipient_list=[email,],
            )
            messages.success(request, "Email de redefinição de senha enviado com sucesso!")
        else:
            messages.error(request, "Nenhum usuário encontrado com o email informado")

    return redirect(view_name)

def logout_site(request):
    logout(request)
    messages.success(request, "Logout efetuado com sucesso!")
    return redirect('index')

def redefinir_senha(request, username, token):

    usuario = User.objects.get(username=username)

    if request.method == "POST":
        if request.POST["senha_1"] != request.POST["senha_2"]:
            return redirect("redefinir_senha", username, token)

        senha = request.POST["senha_1"]
        usuario.set_password(senha)
        usuario.save(force_update=True)

        messages.success(request, "Senha redefinida com sucesso!")
        return redirect("index")

    gerador = PasswordResetTokenGenerator()

    if gerador.check_token(usuario, token):

        context = {"username":username, "token":token}

        return render(request,'inicial/RedefinirSenha.html', context)

def minhas_avaliacoes(request):
    if not request.user.is_authenticated:
        messages.error(request, "Realize login para visualizar suas avaliações")
        return redirect("index")

    buscar2 = BuscarForms()
    filter_form = FilterForms()
    counter = (1, 2, 3, 4, 5)
    avaliacoes = Avaliacao.objects.filter(usuario__exact=request.user.username).order_by("numero")
    context = {"buscar": buscar2, "filter":filter_form, "counter":counter, "avaliacoes":avaliacoes}

    return render(request, "inicial/minhasavaliacoes.html", context)

def pesquisar_avaliacoes(request):
    if not request.user.is_authenticated:
        messages.error(request, "Realize login para visualizar suas avaliações")
        return redirect("index")

    buscar2 = BuscarForms()
    filter_form = FilterForms()
    counter = (1, 2, 3, 4, 5)
    avaliacoes = Avaliacao.objects.filter(usuario__exact=request.user.username).order_by("numero")
    if "hospital" in request.GET:
        avaliacoes = Avaliacao.objects.filter(usuario__exact=request.user.username).filter(hospital__nome__icontains=request.GET["hospital"]).order_by("numero")
    context = {"buscar": buscar2, "filter":filter_form, "counter":counter, "avaliacoes":avaliacoes}

    return render(request, "inicial/minhasavaliacoes.html", context)

def avaliacao_completa(request, avaliacao_id):
    if not request.user.is_authenticated:
        messages.error(request, "Realize login para visualizar suas avaliações")
        return redirect("index")

    buscar2 = BuscarForms()
    filter_form = FilterForms()
    counter = (1, 2, 3, 4, 5)
    avaliacao = get_object_or_404(Avaliacao, pk=avaliacao_id)
    context = {"buscar": buscar2, "filter":filter_form, "counter":counter, "avaliacao":avaliacao}

    return render(request, "inicial/av_completa.html", context)

def meus_dados(request):
    if not request.user.is_authenticated:
        messages.error(request, "Realize login para visualizar seus dados")
        return redirect("index")

    buscar2 = BuscarForms()
    filter_form = FilterForms()
    context = {"buscar": buscar2, "filter":filter_form}

    return render(request, "inicial/meusdados.html", context)

def editar_dados(request):
    if not request.user.is_authenticated:
        messages.error(request, "Realize login para visualizar seus dados")
        return redirect("index")

    if request.method == "POST":
        dados = json.loads(request.POST["dados"])
        dados.pop("dados")
        # print(dados)
        novos_dados = Dados.objects.get(usuario=request.user)

        if dados["nome"] != "":
            novos_dados.nome = dados["nome"]

        if dados["idade"] != "":
            novos_dados.idade = dados["idade"]
        
        if "sexo" in dados:
            novos_dados.sexo = dados["sexo"]

        if dados["profissao"] != "":
            novos_dados.profissao = dados["profissao"]
        
        if dados["endereco"] != "":
            novos_dados.endereco = dados["endereco"]

        if dados["telefone"] != "":
            novos_dados.telefone = dados["telefone"]

        if dados["peso"] != "":
            novos_dados.peso = dados["peso"]

        if dados["altura"] != "":
            novos_dados.altura = dados["altura"]

        if dados["tipo_sanguineo"] != "":
            novos_dados.tipo_sanguineo = dados["tipo_sanguineo"]

        if "sim-nao1" in dados:
            if dados["sim-nao1"] != "nao":
                if "freq1" in dados:
                    novos_dados.fumo_alcool = dados["freq1"]

        if "sim-nao2" in dados:
            if dados["exercicio"] != "":
                novos_dados.exercicio = dados["exercicio"]
                
            if dados["sim-nao2"] != "nao":
                if "freq2" in dados:
                    novos_dados.exercicio_frequencia = dados["freq2"]

        if "sim-nao3" in dados:
            if dados["sim-nao3"] != "nao":
                if "doenca_cronica" in dados:
                    doencas = dados["doenca_cronica"]

                    if isinstance(doencas,list):
                        doencas.pop(0)

                        for i in doencas:
                            print(f"Doença: {i}")

        if "sim-nao4" in dados:
            if dados["sim-nao4"] != "nao":
                sintomas = dados["sintomas"]
                data_sintoma = dados["data_sintoma"]

                if isinstance(sintomas,list) and isinstance(data_sintoma,list):
                    sintomas.pop(0)
                    data_sintoma.pop(0)

                    for i in range(len(sintomas)):
                        print(f"Sintoma: {sintomas[i]} Data: {data_sintoma[i]}")

        if "sim-nao5" in dados:
            if dados["sim-nao5"] != "nao":
                diagnosticos = dados["doencas-diag"]

                if isinstance(diagnosticos, list):
                    diagnosticos.pop(0)

                    for i in diagnosticos:
                        print(f"Diagnosticos: {i}")

        if "sim-nao6" in dados:
            if dados["sim-nao6"] != "nao":
                cirurgias = dados["cirurgias"]
                data_cirurgia = dados["data_cirurgia"]

                if isinstance(cirurgias, list) and isinstance(data_cirurgia, list):
                    cirurgias.pop(0)
                    data_cirurgia.pop(0)

                    for i in range(len(cirurgias)):
                        print(f"Cirurgia: {cirurgias[i]} Data: {data_cirurgia[i]}")

        if "sim-nao7" in dados:
            if dados["sim-nao7"] != "nao":
                motivo = dados["motivo_internacao"]
                tempo_internacao = dados["tempo_internacao"]
                data_internacao = dados["data_internacao"]

                if isinstance(motivo, list) and isinstance(tempo_internacao, list) and isinstance(data_internacao, list):
                    motivo.pop(0)
                    tempo_internacao.pop(0)
                    data_internacao.pop(0)

                    for i in range(len(motivo)):
                        print(f"Motivo: {motivo[i]} Tempo: {tempo_internacao[i]} dias Data: {data_internacao[i]}")

        if "sim-nao8" in dados:
            if dados["sim-nao8"] != "nao":
                if "condicao" in dados and "grau_parentesco" in dados:
                    grau_parentesco = dados["grau_parentesco"]
                    condicao = dados["condicao"]
                    grau_parentesco = list(grau_parentesco)

                    if isinstance(grau_parentesco, list) and isinstance(condicao, list):
                        condicao.pop(0)

                        for i in range(len(grau_parentesco)):
                            print(f"Grau: {grau_parentesco} Condicao: {condicao}")

        if "sim-nao9" in dados:
            if dados["sim-nao9"] != "nao":
                if "medicamento_cp" in dados and "freq_med_cp" in dados and "freq3" in dados: 
                    medicamento_cp = dados["medicamento_cp"]
                    freq_cp = dados["freq_med_cp"]
                    freq3 = dados["freq3"]
                    freq3 = list(freq3)

                    if isinstance(medicamento_cp, list) and isinstance(freq_cp, list) and isinstance(freq3, list):
                        medicamento_cp.pop(0)
                        freq_cp.pop(0)

                        for i in range(len(medicamento_cp)):
                            print(f"Medicamento: {medicamento_cp} Frequência: {freq_cp} {freq3}")

        if "sim-nao10" in dados:
            if dados["sim-nao10"] != "nao":
                if "medicamento_sp" in dados and "freq_med_sp" in dados and "freq4" in dados:
                    medicamento_sp = dados["medicamento_sp"]
                    freq_sp = dados["freq_med_sp"]
                    freq4 = dados["freq4"]
                    freq4 = list(freq4)

                    if isinstance(medicamento_sp, list) and isinstance(freq_sp, list) and isinstance(freq4, list):
                        medicamento_sp.pop(0)
                        freq_sp.pop(0)

                        for i in range(len(medicamento_sp)):
                            print(f"Medicamento: {medicamento_sp} Frequência: {freq_sp} {freq4}")

        novos_dados.save()

    buscar2 = BuscarForms()
    filter_form = FilterForms()
    context = {"buscar": buscar2, "filter":filter_form}

    return render(request, "inicial/editardados.html", context)