# Generated by Django 5.1.6 on 2025-02-17 20:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('portalProfessor', '0006_alter_alunos_foto_perfil'),
    ]

    operations = [
        migrations.AlterField(
            model_name='usuarios',
            name='foto_perfil',
            field=models.ImageField(blank=True, default='fotos_perfil_professor/semFoto.jpg', null=True, upload_to='fotos_perfil_professor'),
        ),
    ]
