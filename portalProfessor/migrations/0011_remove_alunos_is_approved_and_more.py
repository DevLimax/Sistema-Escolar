# Generated by Django 5.1.6 on 2025-02-21 16:59

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('portalProfessor', '0010_notas_notaextra'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='alunos',
            name='is_approved',
        ),
        migrations.CreateModel(
            name='resultado_aluno_approved_disciplinas',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('is_approved', models.BooleanField(default=False)),
                ('nota_final_disciplina', models.FloatField()),
                ('aluno_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='resultados', to='portalProfessor.alunos')),
                ('disciplina_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='resultados', to='portalProfessor.disciplinas')),
            ],
        ),
    ]
