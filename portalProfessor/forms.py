from django import forms
from .models import * 

class loginForm(forms.Form):
    login_input = forms.CharField(label='',widget=forms.TextInput(attrs={'placeholder': 'Email ou Nome de Usuário'}))
    password = forms.CharField(label="",widget=forms.PasswordInput(attrs={'placeholder': 'Senha'}))

class registerForm(forms.Form):
    first_name = forms.CharField(label='',widget=forms.TextInput(attrs={'placeholder': 'Nome'}))
    last_name = forms.CharField(label='',widget=forms.TextInput(attrs={'placeholder': 'Sobrenome'}))
    username = forms.CharField(label='',widget=forms.TextInput(attrs={'placeholder': 'Nome de Usuário'}))   
    email = forms.EmailField(label='',widget=forms.EmailInput(attrs={'placeholder': 'Email'}))
    telefone = forms.CharField(required=False,label='',widget=forms.TextInput(attrs={'placeholder': 'Telefone'}))
    password = forms.CharField(label='',widget=forms.PasswordInput(attrs={'placeholder': 'Senha'}))
    password2 = forms.CharField(label='',widget=forms.PasswordInput(attrs={'placeholder': 'Confirme a Senha'}))

class disciplinaForm(forms.Form):
    nome = forms.CharField(label='Nome',widget=forms.TextInput(attrs={'placeholder': 'Nome da disciplina'}))
    carga_horaria = forms.IntegerField(label='Carga Horária',widget=forms.NumberInput(attrs={'placeholder': 'Carga Horária'}))
    
class New_aluno_form(forms.Form):
    foto_perfil = forms.ImageField(required=False,label='',widget=forms.FileInput(attrs={'placeholder': 'Foto do aluno','class':'file-input'}))
    nome = forms.CharField(label='',widget=forms.TextInput(attrs={'placeholder': 'Nome do aluno'}))
    data_nascimento = forms.DateField(label='',widget=forms.DateInput(attrs={'placeholder': 'Data de Nascimento','type': 'date'}))
    serie = forms.ChoiceField(label='',choices=Alunos.SerieChoices.choices)

class NotasForm(forms.Form):
    bimestre = forms.ChoiceField(label='Bimestre',choices=Notas.BimestreChoices.choices)
    notaParcial = forms.FloatField(label='Nota Parcial',widget=forms.NumberInput(attrs={'placeholder': 'Nota Parcial'}))
    notaBimestral = forms.FloatField(label='Nota Bimestral',widget=forms.NumberInput(attrs={'placeholder': 'Nota Bimestral'}))
    notaConceito = forms.FloatField(label='Nota Conceito',widget=forms.NumberInput(attrs={'placeholder': 'Nota Conceito'}))
    

