# Generated by Django 4.2.1 on 2023-05-05 00:09

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("contas", "0001_initial"),
    ]

    operations = [
        migrations.AlterModelOptions(
            name="myuser",
            options={
                "ordering": ["first_name"],
                "verbose_name": "Usuário",
                "verbose_name_plural": "Usuários",
            },
        ),
    ]