from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.core.paginator import Paginator
from django.contrib import messages
from django.http import HttpResponse
from django.db import IntegrityError
import random
from .forms import *
from .models import *

def professor_register(request):
    forms = registerForm()
    if request.method == 'POST':
        forms = registerForm(request.POST)
        if forms.is_valid():  # Verifica se o formulário é válido
            first_name = forms.cleaned_data['first_name']
            last_name = forms.cleaned_data['last_name']
            username = forms.cleaned_data['username']
            email = forms.cleaned_data['email']
            telefone = forms.cleaned_data['telefone']
            password = forms.cleaned_data['password']
            password2 = forms.cleaned_data['password2']
            if password == password2:
                user = Usuarios(username=username, email=email, telefone=telefone, first_name=first_name, last_name=last_name)
                user.set_password(password)  # Define a senha
                user.save()
                return HttpResponse("Usuário registrado com sucesso!")
            else:
                return HttpResponse("As senhas não coincidem.")
    
    return render(request, 'portalProfessor/register.html', {'forms': forms})

def professor_login(request):
    forms = loginForm()
    if request.method == 'POST':
        forms = loginForm(request.POST)
        if forms.is_valid():  # Verifica se o formulário é válido
            login_input = forms.cleaned_data['login_input']
            password = forms.cleaned_data['password']
            try:
                user = Usuarios.objects.get(username=login_input)
            except Usuarios.DoesNotExist:
                try:
                    user = Usuarios.objects.get(email=login_input)
                except Usuarios.DoesNotExist:
                    try:
                        user = Usuarios.objects.get(telefone=login_input)
                    except Usuarios.DoesNotExist:
                        user = None
            
            if user is not None and user.check_password(password):
                login(request, user) 
                request.session['user'] = user.id
                return redirect('home')
            
            return HttpResponse("Credenciais inválidas.")

    return render(request, 'portalProfessor/login.html', {'forms': forms})

def home(request):
    if request.user.is_authenticated:
        user = request.user
        try:
            disciplina = Disciplinas.objects.get(professor=user.id)
        except Disciplinas.DoesNotExist:
            disciplina = None
        return render(request, 'portalProfessor/home.html', {'disciplina': disciplina})
    return redirect('professor_login')

def logout_view(request):
    logout(request)
    return redirect('professor_login')

def adicionar_disciplina(request):
    forms = disciplinaForm()
    if request.method == 'POST':
        forms = disciplinaForm(request.POST)
        if forms.is_valid():  # Verifica se o formulário é válido
            nome = forms.cleaned_data['nome']
            carga_horaria = forms.cleaned_data['carga_horaria']
            disciplina = Disciplinas(nome=nome, carga_horaria=carga_horaria, professor=request.user)
            disciplina.save()
            return redirect('home')
        
    return render(request, 'portalProfessor/adicionar_disciplina.html', {'forms': forms})

def list_alunos(request,serie):
    if request.user.is_authenticated:
        user = request.user
        try:
            disciplina = Disciplinas.objects.get(professor=user.id)
        except Disciplinas.DoesNotExist:
            disciplina = None
        if disciplina is not None:  
            serie = str(serie)
            alunos_por_serie = Alunos.objects.filter(serie=serie).order_by('nome')
            paginator = Paginator(alunos_por_serie, 6)
            page_number = request.GET.get('page')
            paginator_obj = paginator.get_page(page_number)
            return render(request, 'portalProfessor/alunos.html', {
                'page' : paginator_obj, 'serie' : int(serie)
            })
        return HttpResponse("Você não possui disciplinas cadastradas.")
    return redirect('professor_login')

def new_aluno(request):
    forms = New_aluno_form()
    if request.method == 'POST':
        forms = New_aluno_form(request.POST, request.FILES)
        if forms.is_valid(): 
            foto_perfil = forms.cleaned_data['foto_perfil']
            nome = forms.cleaned_data['nome']
            data_nascimento = forms.cleaned_data['data_nascimento']
            serie = forms.cleaned_data['serie']
            while True:
                try:
                    matricula = random.randint(10000000, 99999999) 
                    aluno = Alunos(nome=nome, matricula=matricula, data_nascimento=data_nascimento, serie=serie)
                    if foto_perfil:
                        aluno.foto_perfil = foto_perfil
                        aluno.save()
                    else:
                        aluno.save()
                    break
                except IntegrityError:
                    print(f'Matricula ja utilizada por um aluno existente!')
                    continue
            return redirect('alunos',1)
    return render(request, 'portalProfessor/novo_aluno.html', {'forms': forms})

def choice_serie(request):
    if request.method == 'POST':
        serie = request.POST.get('serie')
        request.session['serie'] = serie
        return redirect('adicionar_notas')
    return render(request, 'portalProfessor/escolha_serie.html')

def adicionar_notas(request,id,serie):
    aluno = Alunos.objects.get(id=id)
    forms = NotasForm()
    if request.method == 'POST':
        forms = NotasForm(request.POST)
        if forms.is_valid(): 
            aluno = aluno
            disciplina = Disciplinas.objects.get(professor=request.user)
            bimestre = forms.cleaned_data['bimestre']
            if(bimestre == Notas.BimestreChoices.PRIMEIRO_BIMESTRE or bimestre == Notas.BimestreChoices.SEGUNDO_BIMESTRE):
                semestre = Notas.SemestresChoices.PRIMEIRO_SEMESTRE
            else:
                semestre = Notas.SemestresChoices.SEGUNDO_SEMESTRE
            notaParcial = forms.cleaned_data['notaParcial']
            notaBimestral = forms.cleaned_data['notaBimestral']
            notaConceito = forms.cleaned_data['notaConceito']
            try:
                get_nota_in_data = Notas.objects.get(aluno=aluno, disciplina=disciplina, bimestre=bimestre)
            except Notas.DoesNotExist:
                get_nota_in_data = None
            if get_nota_in_data:
                return HttpResponse("Você já adicionou notas para este aluno neste bimestre")
            if notaParcial > 10 or notaParcial < 0 or notaBimestral > 10 or notaBimestral < 0 or notaConceito > 10 or notaConceito < 0:
                return HttpResponse("Você adicionou uma nota invalida, verifique e tente novamente!")
            nota = Notas(aluno=aluno, disciplina=disciplina, bimestre=bimestre, semestre=semestre, notaParcial=notaParcial, notaBimestral=notaBimestral, notaConceito=notaConceito)
            nota.save() 
            return redirect('visualizar_notas',aluno.id,serie)
        
    return render(request, 'portalProfessor/adicionar_notas.html', {'forms': forms, 'aluno':aluno, 'serie':serie})

def visualizar_notas(request, id, serie):
    aluno = Alunos.objects.get(id=id)
    notas = Notas.objects.filter(aluno=aluno, disciplina=Disciplinas.objects.get(professor=request.user))

    check_bimestres = []
    approved_check = None
    for nota in notas:
        if nota.bimestre == Notas.BimestreChoices.PRIMEIRO_BIMESTRE:
            check_bimestres.append(Notas.BimestreChoices.PRIMEIRO_BIMESTRE)
        if nota.bimestre == Notas.BimestreChoices.SEGUNDO_BIMESTRE:
            check_bimestres.append(Notas.BimestreChoices.SEGUNDO_BIMESTRE)
        if nota.bimestre == Notas.BimestreChoices.TERCEIRO_BIMESTRE:
            check_bimestres.append(Notas.BimestreChoices.TERCEIRO_BIMESTRE)
        if nota.bimestre == Notas.BimestreChoices.QUARTO_BIMESTRE:
            check_bimestres.append(Notas.BimestreChoices.QUARTO_BIMESTRE)
    
    if len(check_bimestres) == 4:
        approved_check = True 

    try:
        check_result = Resultado_aluno_approved_disciplinas.objects.get(aluno=aluno, disciplina=Disciplinas.objects.get(professor=request.user))
    except Resultado_aluno_approved_disciplinas.DoesNotExist:
        check_result = None

    return render(request, 'portalProfessor/visualizar_notas.html', {'aluno': aluno, 'query_notas': notas, 'check_bimestres' : approved_check, 'check_result': check_result ,})

def editar_notas(request,id,id_aluno,serie):
    aluno = Alunos.objects.get(id=id_aluno)
    query_notas = Notas.objects.get(id=id)
    if request.method == 'POST':

        newNotaParcial_str = request.POST.get("Parcial")
        newNotaBimestral_str = request.POST.get("Bimestral")
        newNotaConceito_str = request.POST.get("Conceito")
        notaExtra_str = request.POST.get("Extra")

        newNotaParcial = float(newNotaParcial_str) if newNotaParcial_str else None
        newNotaBimestral = float(newNotaBimestral_str) if newNotaBimestral_str else None
        newNotaConceito = float(newNotaConceito_str) if newNotaConceito_str else None
        notaExtra = float(notaExtra_str) if notaExtra_str else None

        if newNotaParcial:
            if newNotaParcial < 0 or newNotaParcial > 10:
                messages.error(request,"Nota Inválida, Tente novamente!")
                return redirect('visualizar_notas', id=id_aluno)
            query_notas.notaParcial = newNotaParcial          
            print(f'Nota Parcial alterada para: {query_notas.notaParcial}')
         
        if newNotaBimestral:
            if newNotaBimestral < 0 or newNotaBimestral > 10:
                messages.error(request,"Nota Inválida, Tente novamente!")
                return redirect('visualizar_notas', id=id_aluno)
            query_notas.notaBimestral = newNotaBimestral
            print(f'Nota Bimestral alterada para: {query_notas.notaBimestral}')
   
        if newNotaConceito:
            if newNotaConceito < 0 or newNotaConceito > 10:
                messages.error(request,"Nota Inválida, Tente novamente!")
                return redirect('visualizar_notas', id=id_aluno)
            query_notas.notaConceito = newNotaConceito
            print(f'Nota Conceito alterada para: {query_notas.notaConceito}')

        if notaExtra:
            if  notaExtra > 10:
                messages.error(request,"Nota Inválida, Tente novamente!")
                return redirect('visualizar_notas', id=id_aluno)
            query_notas.notaExtra = notaExtra
            print(f'Nota Extra alterada para: {query_notas.notaExtra}')
        
        query_notas.save()
        print(f"Nota Final alterada para: {query_notas.notaFinal}")
        
        return redirect('visualizar_notas', id_aluno, serie)
    else:
        return render(request, 'portalProfessor/editar_notas.html', {'query_notas': query_notas,'query_aluno': aluno,'serie':id})
    
def gerar_resultado_final(request, id):
    aluno = Alunos.objects.get(id=id)
    disciplina = Disciplinas.objects.get(professor=request.user)
    query_notas = Notas.objects.filter(aluno=aluno, disciplina=disciplina)
    
    try:
        check_exist_result = Resultado_aluno_approved_disciplinas.objects.get(aluno=aluno, disciplina=disciplina)
    except Resultado_aluno_approved_disciplinas.DoesNotExist:
        check_exist_result = None
    
    if check_exist_result:
        return HttpResponse("Resultado ja gerado para esse aluno!")

    resultado = Resultado_aluno_approved_disciplinas(aluno=aluno, disciplina=disciplina)
    for notas in query_notas:
        if notas.bimestre == Notas.BimestreChoices.PRIMEIRO_BIMESTRE:
            resultado.setter_notaBimestre1(nota=notas.notaFinal)
        if notas.bimestre == Notas.BimestreChoices.SEGUNDO_BIMESTRE:
            resultado.setter_notaBimestre2(nota=notas.notaFinal)
        if notas.bimestre == Notas.BimestreChoices.TERCEIRO_BIMESTRE:
            resultado.setter_notaBimestre3(nota=notas.notaFinal)
        if notas.bimestre == Notas.BimestreChoices.QUARTO_BIMESTRE:
            resultado.setter_notaBimestre4(nota=notas.notaFinal)

    resultado.gerar_resultado()
    resultado.save()
    return render(request, 'portalProfessor/resultado_gerado.html', {'aluno':aluno,'disciplina':disciplina,'resultado':resultado})
    
def resultado_view(request,id):
    aluno = Alunos.objects.get(id=id)
    disciplina = Disciplinas.objects.get(professor=request.user)
    query_resultado = Resultado_aluno_approved_disciplinas.objects.get(aluno=aluno,disciplina=disciplina)

    if query_resultado:
        return render(request, 'portalProfessor/resultado_gerado.html', {'resultado':query_resultado, 'aluno':aluno, 'disciplina':disciplina})
    



