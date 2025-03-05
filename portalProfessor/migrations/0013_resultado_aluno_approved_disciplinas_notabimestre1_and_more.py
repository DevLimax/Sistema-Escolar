# Generated by Django 5.1.6 on 2025-02-21 17:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('portalProfessor', '0012_rename_aluno_id_resultado_aluno_approved_disciplinas_aluno_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='resultado_aluno_approved_disciplinas',
            name='notaBimestre1',
            field=models.FloatField(default=0, null=True),
        ),
        migrations.AddField(
            model_name='resultado_aluno_approved_disciplinas',
            name='notaBimestre2',
            field=models.FloatField(default=0, null=True),
        ),
        migrations.AddField(
            model_name='resultado_aluno_approved_disciplinas',
            name='notaBimestre3',
            field=models.FloatField(default=0, null=True),
        ),
        migrations.AddField(
            model_name='resultado_aluno_approved_disciplinas',
            name='notaBimestre4',
            field=models.FloatField(default=0, null=True),
        ),
        migrations.AlterField(
            model_name='resultado_aluno_approved_disciplinas',
            name='is_approved',
            field=models.BooleanField(default=False, null=True),
        ),
        migrations.AlterField(
            model_name='resultado_aluno_approved_disciplinas',
            name='nota_final_disciplina',
            field=models.FloatField(default=0, null=True),
        ),
    ]
