# Generated by Django 3.2.6 on 2021-09-09 09:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('chat', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='thread',
            name='name',
            field=models.CharField(max_length=50, null=True, unique=True),
        ),
    ]
