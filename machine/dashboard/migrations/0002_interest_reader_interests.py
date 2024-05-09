# Generated by Django 4.2.11 on 2024-05-07 23:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dashboard', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Interest',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=100)),
            ],
        ),
        migrations.AddField(
            model_name='reader',
            name='interests',
            field=models.ManyToManyField(blank=True, to='dashboard.interest'),
        ),
    ]
