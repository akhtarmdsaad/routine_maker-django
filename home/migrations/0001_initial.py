# Generated by Django 3.1 on 2023-05-11 03:30

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Cell',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=50)),
                ('start_time', models.TimeField(null=True)),
                ('end_time', models.TimeField(null=True)),
                ('needed_time', models.TimeField(null=True)),
                ('consistency', models.TimeField(null=True)),
                ('preferred_time_list', models.TextField()),
            ],
        ),
    ]
