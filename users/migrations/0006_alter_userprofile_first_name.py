# Generated by Django 3.2.2 on 2021-05-21 21:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0005_emailverifycode'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userprofile',
            name='first_name',
            field=models.CharField(blank=True, max_length=150, verbose_name='first name'),
        ),
    ]
