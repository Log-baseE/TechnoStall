# Generated by Django 2.0.7 on 2018-08-01 13:03

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('tsmanager', '0009_stallkeeper'),
    ]

    operations = [
        migrations.CreateModel(
            name='TSUser',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('major', models.CharField(choices=[('TIF', 'Informatics'), ('SI', 'Information Systems')], max_length=3)),
                ('active', models.BooleanField(default=True)),
                ('role', models.CharField(choices=[('SL', 'Stallkeeper'), ('SA', 'Stall Admin')], max_length=2)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.RemoveField(
            model_name='stallkeeper',
            name='user',
        ),
        migrations.AlterField(
            model_name='restock',
            name='restock_amount',
            field=models.PositiveIntegerField(),
        ),
        migrations.DeleteModel(
            name='Stallkeeper',
        ),
    ]
