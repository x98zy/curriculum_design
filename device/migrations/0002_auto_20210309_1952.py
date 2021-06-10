# Generated by Django 2.0 on 2021-03-09 11:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('device', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='device',
            name='status',
            field=models.CharField(choices=[('OFFLINE', '离线'), ('ONLINE', '在线'), ('ABNORMAL', '异常')], default='OFFLINE', max_length=20, verbose_name='设备状态'),
        ),
    ]
