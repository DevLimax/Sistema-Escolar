from django.urls import path
from .views import *


urlpatterns = [
    path('', professor_login, name='professor_login'),
    path('professor_register/', professor_register, name='professor_register'),
    path('home/', home, name='home'),
    path('logout/', logout_view, name='logout'),
    path('disciplina/', adicionar_disciplina, name='adicionar_disciplina'),
    path('alunos/<int:serie>', list_alunos, name='alunos'),
    path('aluno/', new_aluno, name='novo_aluno'),
    path('add-notas/<int:id>/<int:serie>', adicionar_notas, name='adicionar_notas'),
    path('visualizar-notas/<int:id>/<int:serie>',visualizar_notas, name='visualizar_notas'),
    path('editar-notas/<int:id>/<int:id_aluno>/<int:serie>',editar_notas, name='editar_notas'),
    path('gerar-resultado/<int:id>', gerar_resultado_final, name="gerar_resultado"),
    path('resultado/<int:id>', resultado_view, name='resultado')
]

