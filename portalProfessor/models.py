from django.db import models
from django.contrib.auth.models import AbstractUser
from django.conf import settings

class Usuarios(AbstractUser):
    foto_perfil = models.ImageField(upload_to='fotos_perfil_professor', null=False, blank=True, default='fotos_perfil_professor/semFoto.jpg') 
    telefone = models.CharField(max_length=100, null=True, blank=True, unique=True)

    def __str__(self):
        return self.username
    

class Alunos(models.Model):

    class SerieChoices(models.TextChoices):
        PRIMEIRA_SERIE = '1', '1º Ano'
        SEGUNDA_SERIE = '2', '2º Ano'
        TERCEIRA_SERIE = '3', '3º Ano'

    id = models.AutoField(primary_key=True)
    foto_perfil = models.ImageField(upload_to='fotos_perfil_aluno', null=False, blank=True, default='fotos_perfil_aluno/semFoto.jpg')
    nome = models.CharField(max_length=200, null=False)
    data_nascimento = models.DateField(null=False)
    matricula = models.CharField(max_length=200, null=False, unique=True)
    serie = models.CharField(max_length=200, null=False, choices=SerieChoices.choices)

    def __str__(self):
        return self.nome
    

class Disciplinas(models.Model):

    class DisciplinasChoices(models.TextChoices):
        pass

    id = models.AutoField(primary_key=True)
    nome = models.CharField(max_length=200, null=False)
    carga_horaria = models.IntegerField(null=False)
    professor = models.ForeignKey(settings.AUTH_USER_MODEL ,on_delete=models.CASCADE, related_name="disciplinas")
    alunos = models.ManyToManyField(Alunos, related_name="disciplinas")

    def __str__(self):
        return self.nome
    

class Notas(models.Model):

    class BimestreChoices(models.TextChoices):
        PRIMEIRO_BIMESTRE = '1', '1º Bimestre'
        SEGUNDO_BIMESTRE = '2', '2º Bimestre'
        TERCEIRO_BIMESTRE = '3', '3º Bimestre'
        QUARTO_BIMESTRE = '4', '4º Bimestre'
    
    class SemestresChoices(models.TextChoices):
        PRIMEIRO_SEMESTRE = '1', '1º Semestre'
        SEGUNDO_SEMESTRE = '2', '2º Semestre'

    id = models.AutoField(primary_key=True)
    aluno = models.ForeignKey(Alunos, on_delete=models.CASCADE, related_name="notas")
    disciplina = models.ForeignKey(Disciplinas, on_delete=models.CASCADE, related_name="notas")
    notaParcial = models.FloatField(null=False, blank=False)
    notaBimestral = models.FloatField(null=False, blank=False)
    notaConceito = models.FloatField(null=False, blank=False)
    notaExtra = models.FloatField(null=False, blank=True, default=0.0)
    notaFinal = models.FloatField(null=False, default=0.0)
    bimestre = models.CharField(max_length=200, choices=BimestreChoices.choices, null=False)
    semestre = models.CharField(max_length=200, choices=SemestresChoices.choices, null=False)
    data_criacao = models.DateTimeField(auto_now_add=True)


    def save(self, *args, **kwargs):
        self.notaFinal = (self.notaBimestral + self.notaParcial + self.notaConceito + self.notaExtra) / 3
        self.notaFinal = round(self.notaFinal, 1)
        if self.notaFinal > 10:
            self.notaFinal = 10.0
        super().save(*args, **kwargs)

class Resultado_aluno_approved_disciplinas(models.Model):
    id = models.AutoField(primary_key=True)
    aluno = models.ForeignKey(Alunos, on_delete=models.CASCADE, related_name="resultados")
    disciplina = models.ForeignKey(Disciplinas, on_delete=models.CASCADE, related_name="resultados")
    is_approved = models.BooleanField(null=True, default=False)
    notaBimestre1 = models.FloatField(null=True, default=0)
    notaBimestre2 = models.FloatField(null=True, default=0)
    notaBimestre3 = models.FloatField(null=True, default=0)
    notaBimestre4 = models.FloatField(null=True, default=0)
    nota_final_disciplina = models.FloatField(null=True, default=0)

    def setter_notaBimestre1(self, nota: float):
        try:
            self.notaBimestre1 = nota
            print(f"Nota inserida {self.notaBimestre1}")
            return
        
        except ValueError:
            raise("Nota Invalida!")
        
    def setter_notaBimestre2(self, nota: float):
        try:
            self.notaBimestre2 = nota
            print(f"Nota inserida {self.notaBimestre2}")
            return
        
        except ValueError:
            raise("Nota Invalida!")
        
    def setter_notaBimestre3(self, nota: float):
        try:
            self.notaBimestre3 = nota
            print(f"Nota inserida {self.notaBimestre3}")
            return
        
        except ValueError:
            raise("Nota Invalida!")
        
    def setter_notaBimestre4(self, nota: float):
        try:
            self.notaBimestre4 = nota
            print(f"Nota inserida {self.notaBimestre4}")
            return
        
        except ValueError:
            raise("Nota Invalida!")
    
    def gerar_resultado(self):
        sumNotas = self.notaBimestre1 + self.notaBimestre2 + self.notaBimestre3 + self.notaBimestre4
        media = sumNotas / 4
        if media >= 6:
            self.is_approved = True
            self.nota_final_disciplina = round(media, 1)
            return
        else:
            self.is_approved = False
            self.nota_final_disciplina = round(media, 1)
            return


    


    
    



    