# Generated by Django 3.0.5 on 2020-11-13 13:27

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='ITjob',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('job_title', models.CharField(max_length=210)),
                ('job_intro', models.TextField(default='')),
                ('job_description', models.TextField(default='')),
                ('job_date', models.TextField(default='')),
                ('job_link', models.TextField()),
            ],
        ),
    ]
