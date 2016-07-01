# -*- coding: utf-8 -*-
# Generated by Django 1.9.5 on 2016-05-13 17:40
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('operators', '0001_initial'),
        ('scenarios', '0001_initial'),
        ('vnfs', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Deployment',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=120)),
                ('file', models.FileField(blank=True, null=True, upload_to='deployments/')),
                ('start', models.TimeField(blank=True, null=True)),
                ('stop', models.TimeField(blank=True, null=True)),
                ('price', models.FloatField(blank=True, default=0, null=True)),
                ('rb', models.IntegerField(blank=True, default=0, null=True)),
                ('update', models.DateTimeField(auto_now=True)),
                ('timestamp', models.DateTimeField(auto_now_add=True)),
                ('area', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='scenarios.OArea')),
                ('propietario', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='operators.Operator')),
            ],
            options={
                'ordering': ['-timestamp', '-update'],
            },
        ),
        migrations.CreateModel(
            name='Nvf',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=20)),
                ('freC_DL', models.IntegerField(blank=True, null=True)),
                ('color_DL', models.CharField(blank=True, max_length=20, null=True)),
                ('BW_DL', models.IntegerField(blank=True, null=True)),
                ('rb', models.IntegerField(blank=True, null=True)),
                ('Pt', models.FloatField(blank=True, null=True)),
                ('freC_UL', models.IntegerField(blank=True, null=True)),
                ('color_UL', models.CharField(blank=True, max_length=20, null=True)),
                ('BW_UL', models.IntegerField(blank=True, null=True)),
                ('radio', models.CharField(blank=True, default=0, max_length=120, null=True)),
                ('static_labels', models.CharField(blank=True, max_length=400, null=True)),
                ('static_cpu', models.CharField(blank=True, max_length=400, null=True)),
                ('static_ram', models.CharField(blank=True, max_length=400, null=True)),
                ('static_net', models.CharField(blank=True, max_length=400, null=True)),
                ('users', models.IntegerField(blank=True, default=0, null=True)),
                ('update', models.DateTimeField(auto_now=True)),
                ('timestamp', models.DateTimeField(auto_now_add=True)),
                ('bts', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='scenarios.Bts')),
                ('deploy', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='deployments.Deployment')),
                ('operator', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='operators.Operator')),
                ('vnf', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='vnfs.Vnf')),
            ],
            options={
                'ordering': ['-timestamp', '-update'],
            },
        ),
    ]
