# Generated by Django 4.0.2 on 2022-02-21 20:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('API', '0004_alter_usuario_hobbies'),
    ]

    operations = [
        migrations.AlterField(
            model_name='usuario',
            name='password',
            field=models.CharField(max_length=50),
        ),
    ]
